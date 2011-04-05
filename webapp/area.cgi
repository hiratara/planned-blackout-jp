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
	my $view = decide_view $query;
	my $criteria = do {
		my ($city) = grep {$_ ne ''} $query->param('city');  # choice one
		$city = '' unless defined $city;
		force_decode($city);
	};
	my $titlename = $criteria;
	my $template = $view eq 'm' ? 'aream.html' : 'areapc.html';

	my @dates = map {date_str(time + DAY_SECONDS * $_)} 0 .. 2;

	my $regex_city;
	if ($criteria =~ /^(\d{3})-?(\d{4})$/) {
		# called by zip code
		my $zipcode = "$1$2";
		my @cities = search_zip $zipcode;

		unless (@cities) {
			return process_template("$base_dir/$template", {
				title => $titlename, dates => \@dates,
				areas => [], schedule_map => {}, 
				error_message => qq/郵便番号"$zipcode"は見つかりませんでした。/,
			});
		}

		$regex_city = join '|', map { 
			quotemeta(normalize_address $_) 
		} @cities;
	} else {
		$regex_city = normalize_address $criteria;
	}

	my $getgroup = $query->param('gid') || '';
	$getgroup = '' unless $getgroup =~/^[1-5]$/;
	my $getgroup_sub = $query->param('gids') || '';
	$getgroup_sub = '' unless $getgroup_sub =~/^[A-E]$/;

	my $areas = search_area(
		regex_city => $regex_city,
		group      => $getgroup,
		subgroup   => $getgroup_sub,
	);

	my $runtable  = read_runtable;
	my $timetable = read_timetable;

	my $error_message;
	if (! @$areas) {
		$error_message = "計画停電のないエリアです。";
	} elsif (@$areas > 400) {
		$error_message = "該当地域が多すぎです。詳細の地域名を入力してください。";
	}

	return process_template("$base_dir/$template", {
		title => $titlename, 
		dates => \@dates, 
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
