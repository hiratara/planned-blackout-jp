#!/usr/bin/perl

########################
# history of updates
# 2011/3/29 00:00 V1.200 HTMLを外部ファイル化。コード整理。(hiratara)
# 2011/3/28 16:10 V1.14alpha 停電実行ステータス対応(runtable.txtの読み込み)、ちょっと高速化処理(nanakochi123456)
# 2011/3/26 17:50 V1.131(nanakochi123456)入力文字列の正規化、グループ拡張、バージョン番号の拡張。(tnx:nanakochi123456)
# 2011/3/21 17:00 V1.130(nyatakasan,hiratara) 時間表取得方法を変更(timetable.txtの読み込み)。(tnx:nyatakasan,hiratara)
# 2011/3/20 23:02 V1.122 漢字コード変換を変更。短い地名でも検索できます(tnx:hiratara)。
# 2011/3/19 00:25 V1.121 引数として、comm=verを渡すとバージョン番号を戻すように変更。
# 2011/3/18 14:25 V1.12 postからgetに変更(tnx:nanakochi123456)。18日以降の表示対応
# 2011/3/15 20:24 V1.112 住所ソート表示、16-18日の表示対応
# 2011/3/15 07:50 V1.111 該当件数を表示するように変更、表示上限を400件に拡大
# 2011/3/14 23:20 V1.110 グループ番号で絞り込めるように変更 (tnx:eOhirune)
# 2011/3/14 10:25 V1.100 負荷軽減できるように軽めに調整
# 2011/3/14 03:06 V1.005 地区名が該当しないときのメッセージの表示を変更 (tnx:sunka_)
# 2011/3/14 02:08 V1.004 検索文字列中の空白を無視するように変更 (tnx:mnrohk)
# 2011/3/14 00:35 V1.003 タイトルタグの脱字修正
# 2011/3/13 23:49 V1.002 第三グループの時間表示ミスを修正 (tnx:tukanana)
# 2011/3/13 23:43 V1.001 詳細地域名入れたときの検索対応 (tnx:hamadalabs)
# 2011/3/13 23:17 initial release(mnakajim)


use strict;
#use warnings;
use utf8;
use FindBin qw($Bin);
BEGIN { require "$Bin/fatlib.pl" }
use Encode qw/decode_utf8/;
use Encode::Guess;
use CGI;
use Text::MicroTemplate::File;
use constant DAY_SECONDS => 24 * 60 * 60;

binmode STDOUT, ":utf8";

sub date_str($) {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

sub read_timetable() {
	my %timetable;

	open my $fh, '<:utf8', "$Bin/timetable.txt" or die $!;
	while (<$fh>) {
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

sub read_runtable() {
	my %runtable;

	open my $fh, '<:utf8', "$Bin/runtable.txt" or die $!;
	while (<$fh>) {
		chomp;
		my ($date, $group, $state) = split /\t/, $_;
		$runtable{$date}{$group} = $state;
	}
	close $fh;

	return \%runtable;
}

sub search_zip($) {
	my $zip = shift;  # assumes that $zip has no hyphens.

	my @cities;
	open my $fh, '<:utf8', "$Bin/yubin.csv" or die $!;
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

sub force_decode($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? $enc->decode($str) : decode_utf8($str);
}

sub addnor($) {
	my $add = shift;
	$add =~ tr/0-9がケヶのノ　 /０-９ケケケのの/d;
	return $add;
}

sub gettimetablever{
	open my $in, '<:utf8', "$Bin/timetable.txt" or die $!;
	while(<$in>) {
		chomp;
		my ($firm,$ver)=split(/\t/,$_);
		if($firm eq "V") {
			return $ver;
		}
	}
	return '--';
}

sub getareatablever{
	open my $in, '<:utf8', "$Bin/all.all" or die $!;
	while (<$in>) {
		chomp;
		my ($field,$ver)=split(/\t/,$_);
		if($field eq "version") {
			return $ver;
		}
	}
	return '--';
}

my $query=new CGI;
my $comm=$query->param('comm');
my $criteria = force_decode($query->param('city'));
my $titlename = $criteria;

my $regex_city;
if ($criteria =~ /^(\d{3})-?(\d{4})$/) {
	# called by zip code
	my $zipcode = "$1$2";
	$regex_city = join '|', map { quotemeta(addnor $_) } search_zip $zipcode;
} else {
	$regex_city = addnor $criteria;
}

my $getgroup=int($query->param('gid'));
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}
my $ver='1.200';
my $auth='mnakajim';

if ($comm=~ m/ver/gi) {
	my $timetable = gettimetablever();
	my $areatable = getareatablever();
	print $query->header("text/plain");
	print "area.cgi : $ver($auth)\n";
	print "timetable.txt : $timetable\n";
	print "areatable.txt : $areatable\n";
	exit;
}


open my $in, '<:utf8', "$Bin/all.all" or die $!;

my @results;

my $runtable = read_runtable;
my $timetable = read_timetable;
my @dates = map {date_str(time + DAY_SECONDS * $_)} 0 .. 2;

while (<$in>) {
	chomp;
	my ($area1,$area2,$area3,$num,$grp)=split (/\t/,$_);
	my $firm = 'T';  # XXX 東電。現状の実装では固定。

	next if $area1 eq 'version';

	my $areaorg = addnor "$area1$area2$area3";

	next if $getgroup && $num != $getgroup;
	next unless $areaorg =~ m/$regex_city/;

	my @hour_refs = map {
		my $hours = $timetable->{$firm}{$_}{$num};
		my $run_str = $runtable->{$_}{"$num\-$grp"} || '-';
		my $hours_str = $hours ? join(', ', @$hours) : '-';
		{hours_str => $hours_str, run_str => $run_str};
	} @dates;

	push @results, {
		tdfk => $area1, 
		shiku => $area2, 
		machiaza => $area3,
		hour_refs => \@hour_refs,
		num => $num, grp => $grp,
	};
}
close $in;

my $error_message;
if (! @results) {
	$error_message = "計画停電のないエリアです。";
} elsif (@results > 400) {
	$error_message = "該当地域が多すぎです。詳細の地域名を入力してください。";
}

my $mtf = Text::MicroTemplate::File->new;
print $query->header("text/html; charset=utf-8");
print $mtf->render_file(
	"$Bin/area.html", 
	$titlename, \@dates, \@results, $error_message
);
