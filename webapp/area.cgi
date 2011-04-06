#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use File::Basename qw/dirname basename/;
BEGIN { require (dirname(__FILE__) . "/fatlib.pl") }
use Encode qw/decode_utf8/;
use Encode::Guess;
use CGI;
use PlannedBlackoutJP;
use PlannedBlackoutJP::Util qw/is_galapagos/;
use Text::MicroTemplate qw/render_mt/;
use Text::MicroTemplate::File;
use constant DAY_SECONDS => 24 * 60 * 60;

my $base_dir = dirname(__FILE__);
binmode STDOUT, ":utf8";

sub date_str($) {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

sub safe_open($) {
	my $file = shift;
	my $result = open my $fh, '<:utf8', "$file";
	unless ($result) {
		warn "$!: $file";
		die basename($file) . " can't read.\n";
	}
	return $fh;
}

sub process_template($$) {
	my ($template, $args) = @_;

	my $mtf = Text::MicroTemplate::File->new(
		tag_start => '<%', tag_end => '%>', line_start => '%',
	);
	return $mtf->render_file($template, $args);
}

sub force_decode($) {
	my $str = shift;
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? $enc->decode($str) : decode_utf8($str);
}

sub normalize_address($) {
	my $add = shift;
	$add =~ tr/0-9がケヶのノ　 /０-９ケケケのの/d;

	# remove '字' and '大字'
	$add =~ s/([市区町村])大?字/$1/;

	return $add;
}

sub read_timetable() {
	my %timetable;

	my $fh = safe_open "$base_dir/timetable.txt";
	while (<$fh>) {
		chomp;
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		next if $firm eq 'V'; # skip version line
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

sub read_runtable() {
	my %runtable;

	my $fh = safe_open "$base_dir/runtable.txt";
	while (<$fh>) {
		chomp;
		my ($date, $group, $state) = split /\t/, $_;
		next if $date eq 'V'; # skip version line
		$runtable{$date}{$group} = $state;
	}
	close $fh;

	return \%runtable;
}

sub search_zip($) {
	my $zip = shift;  # assumes that $zip has no hyphens.

	my @cities;
	my $fh = safe_open "$base_dir/yubin.csv";
	while (<$fh>) {
		chomp;
		my ($cur_zip, $left) = split /\t/, $_, 2;
		if ($zip == $cur_zip) {
			$left =~ tr/\t//d;
			push @cities, $left;
		}
	}
	close $fh;

	return @cities;
}

sub search_area {
	my %criteria = @_;
	my $regex_city = delete $criteria{regex_city};
	my $group      = delete $criteria{group};
	my $subgroup   = delete $criteria{subgroup};

	my @areas;
	my $in = safe_open "$base_dir/all.all";
	while (<$in>) {
		chomp;
		my ($area1, $area2, $area3, $gr, $subgr)=split (/\t/,$_);
		my $firm = 'T';  # XXX 東電。現状の実装では固定。

		next if $area1 eq 'version';

		my $areaorg = normalize_address "$area1$area2$area3";

		next if $group && $gr != $group;
		next if $subgroup && $subgr ne $subgroup;
		next if $regex_city && $areaorg !~ m/$regex_city/;

		push @areas, {
			tdfk => $area1, 
			shiku => $area2, 
			machiaza => $area3,
			firm => $firm, group => $gr, subgroup => $subgr,
		};
	}

	\@areas;
}

sub find_version_line($$) {
	my ($file, $key) = @_;
	my $in = safe_open "$base_dir/$file";

	while (<$in>) {
		chomp;
		my ($cur_key, $left) = split /\t/, $_, 2;
		if ($cur_key eq $key) {
			return $left;
		}
	}

	return '--';
}

sub decide_view($) {
	my $query = shift;
	$query->param('view') || (is_galapagos(\%ENV) ? 'm' : 'p');
}

sub main_handler {
	my $query = shift;

	my $criteria = do {
		my ($city) = grep {$_ ne ''} $query->param('city');  # choice one
		$city = '' unless defined $city;
		force_decode($city);
	};
	my $getgroup = $query->param('gid') || '';
	$getgroup = '' unless $getgroup =~/^[1-5]$/;
	my $getgroup_sub = $query->param('gids') || '';
	$getgroup_sub = '' unless $getgroup_sub =~/^[A-E]$/;

	# Correct parameters for the template.
	my $view = decide_view $query;
	my $template = $view eq 'm' ? 'aream.html' : 'areapc.html';
	my %params_base = (
		title => $criteria,
		dates => [map {date_str(time + DAY_SECONDS * $_)} 0 .. 2],
		areas => [],
	);

	my $regex_city;
	if ($criteria =~ /^(\d{3})-?(\d{4})$/) {
		# called by zip code
		my $zipcode = "$1$2";
		my @cities = search_zip $zipcode;

		unless (@cities) {
			return process_template("$base_dir/$template", {
				%params_base,
				error_message => qq/郵便番号"$zipcode"は見つかりませんでした。/,
			});
		}

		$regex_city = join '|', map { 
			quotemeta(normalize_address $_) 
		} @cities;
	} else {
		$regex_city = normalize_address $criteria;
	}

	my $areas = search_area(
		regex_city => $regex_city,
		group      => $getgroup,
		subgroup   => $getgroup_sub,
	);

	my $error_message;
	if (! @$areas) {
		$error_message = "計画停電のないエリアです。";
	} elsif (@$areas > 400) {
		$error_message = "該当地域が多すぎです。詳細の地域名を入力してください。";
	}

	my $runtable  = read_runtable;
	my $timetable = read_timetable;

	return process_template("$base_dir/$template", {
		%params_base,
		areas => $areas, 
		get_hours_str => sub {
			my ($date, $area) = @_;
			my $hours = $timetable->{$area->{firm}}{$date}{$area->{group}};
			$hours ? join(',', @$hours) : '-';
		},
		get_run_str => sub {
			my ($date, $area) = @_;
			my $group_str = "$area->{group}-$area->{subgroup}";
			$runtable->{$date}{$group_str} || '-';
		},
		error_message => $error_message,
	});
}

sub version_handler {
	my $query = shift;
	my $auth = 'mnakajim';

	my $timetable = find_version_line 'timetable.txt', 'V';
	my $areatable = find_version_line 'all.all', 'version';
	my $runtable = find_version_line 'runtable.txt', 'V';
	return <<__BODY__ => "text/plain";
area.cgi : $PlannedBlackoutJP::VERSION($auth)
timetable.txt : $timetable
areatable.txt : $areatable
runtable.txt : $runtable
__BODY__
}


my $query = CGI->new;
my $comm = $query->param('comm') || '';

my $handler = $comm=~ m/ver/gi ? \&version_handler : \&main_handler;

my ($body, $content_type) = eval { $handler->($query) };
if ($@) {
	warn $@;
	print $query->header("text/html; charset=UTF-8");
	print render_mt(<<'__HTML__', $@, decide_view($query))->as_string;
<html><head><title>Error</title></head>
<body><h1>Error!</h1><hr /><h2><?= $_[0] ?></h2><br />
<a href="index.cgi?view=<?= $_[1] ?>">Return</a></body></html>
__HTML__

} else {
	print $query->header($content_type || "text/html; charset=UTF-8");
	print $body;
}

__END__

=encoding utf8

=head1 NAME

area.cgi - 計画停電の検索

=head1 DESCRIPTION

計画停電の時間を住所、郵便番号、停電グループなどの条件から検索する。

=head1 HANDLERS

このCGIでは、リクエストパラメータ"comm="の値によって実行されるハンドラが
決まる。各ハンドラは、CGIオブジェクトを受け取り、出力文字列とContent-Type
を返す関数である。

  my ($body, $content_type) = $handler->(CGI->new);

Content-Typeの省略時には、"text/html; charset=utf8"となる。

=head2 main_handler (デフォルト)

今日〜３日後までの計画停電の予定を検索する。検索条件として以下のリクエスト
パラメータを受け取る。

=over

=item view

検索結果の出力形式を指定する。"m"(携帯)または"p"(PC)の値を指定できる。
省略時はUserAgentにより自動的に決定される。

=item city

検索したい文字列を指定する。"0000000"または"000-0000"の形式の場合は郵便番号
を指定した物と見なされる。それ以外の場合は、住所の一部分が指定されたと見なす。

文字列はUTF-8またはShift_JISにて指定する(後者はAU携帯のため)。

=item gid

検索したい計画停電のグループを数値で指定する。

=item gids

検索したい計画停電のサブグループをアルファベット一文字で指定する。

=back

検索結果が多すぎる場合には、結果を出力せずエラーを表示して終了する。

=head2 version_handler (comm=ver)

CGI、データファイルのバージョン情報を出力する。

=head1 FUNCTIONS

=head2 date_str

epoch秒を"YYYY-MM-DD"という表現の文字列にする。

  my $date = date_str time;

=head2 safe_open

open関数と同等の処理を行う。openに失敗した場合には、ブラウザに表示されても
差し支えない文字列を例外として投げる。

  my $fh = safe_open "/path/to/your_file.txt";

=head2 process_template

Text::MicroTemplate::Fileのrender_fileのショートカット。
与えられたファイルをテンプレートとし、引数を渡して実行する。

  process_template "/path/to/template.txt", 
                   {arg1 => $arg1, arg2 => $arg2, ...};

=head2 force_decode

文字コードが不明確な文字列を、Perlの内部文字列へデコードする。
特にAUの携帯電話ではShift_JISによってフォームデータをエスケープするため、
これをguess_encodingによって適切に判定する。

  my $string = force_decode $unknown_bytes;

=head2 normalize_address

住所文字列を正規化する。同じ住所を表す異なる文字列を入力した場合に、
同一の文字列が生成されることを目標とする。

  # 以下はすべて"茅ケ崎市香川１丁目"となる。
  my $addr1 = normalize_address "茅ヶ崎市香川１丁目";
  my $addr2 = normalize_address "茅が崎市香川１丁目";
  my $addr3 = normalize_address "茅ケ崎市　香川1丁目";

=head2 read_timetable

計画停電時間ファイルを読み込み、hash-refとして返す。
ファイル内の各列がキーとなり、停電時間の列をarray-refとしたものが値となる。
バージョン行は出力に含まない。

  my $table = read_timetable;

  # 東電(T)の4/1の3グループの停電時間
  my $hours = $table->{T}{'2011-04-01'}{3};

  # "18:20-22:10" などを表示
  print $_, "\n" for @$hours;

=head2 read_runtable

計画停電実績ファイルを読み込み、hash-refとして返す。
ファイル内の各列がキーとなり、実績を表す列が値となる。
バージョン行は出力に含まない。

  my $table = read_runtable;

  # 4/1の3-Cグループの停電実績
  my $result_str = $table->{'2011-04-01'}{"3-C"};

  # "実施せず" などを表示
  print $result_str, "\n";

=head2 search_zip

郵便番号ファイルより、該当する郵便番号の住所を検索して返す。
郵便番号はハイフンを含めない7桁の数字を入力する。出力される住所文字列は、
郵便番号ファイル内の都道府県、市区、町字をすべて連結したものとなる。

  my @cities = search_zip "2080001";

  # "東京都武蔵村山市中藤" などを表示
  print $_, "\n" for @cities;

=head2 search_area

グループ分けファイルより、検索条件に合致する行を返す。

  my $areas = search_area regex_city => '横浜市|川崎市';

  for (@$areas) {
      print $areas->{tdfk}    , "\n"; # "神奈川県" など
      print $areas->{shiku}   , "\n"; # "川崎市麻生区" など
      print $areas->{machiaza}, "\n"; # "岡上" など
      print $areas->{firm}    , "\n"; # "T"(東京電力) など
      print $areas->{group}   , "\n"; # "2" など
      print $areas->{subgroup}, "\n"; # "D" など
  }

検索条件は、以下の項目をand検索として指定する。

=over

=item regex_city

住所文字列を正規表現で指定する。normalize_address()にて正規化された住所に
マッチする正規表現を指定する必要がある。

=item group

グループ番号を数値で指定する。

=item subgroup

サブグループ番号をアルファベットで指定する。

=back

=head2 find_version_line

指定したTSVファイルからバージョン番号行を見つけ、バージョン番号を返す。
バージョン番号行を見つけるため、バージョン番号を表す行の最も左の列の値を
指定する必要がある。

  my $version_string = find_version_line "/pathto/tsv.txt", "key_of_ver_line";

=head2 decide_view

このリクエストにおける表示形式を返す。携帯向け表示を行う場合は"m"、
PC向け表示を行う場合は"p"が返される。表示形式はUserAgentなどによって
自動的に決定されるが、HTTPリクエストのパラメータ"view="にて直接指定
することもできる。

  my $view = decide_view(CGI->new);

=cut

