#!/usr/bin/perl

########################
# history of updates
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
use FindBin qw($Bin);
BEGIN { require "$Bin/fatlib.pl" }
use Encode qw/encode_utf8 decode_utf8/;
use Encode::Guess;
use CGI;
use Text::MicroTemplate::File;
use constant DAY_SECONDS => 24 * 60 * 60;

sub date_str($) {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

sub read_timetable() {
	my %timetable;

	open my $fh, '<', "$Bin/timetable.txt" or die $!;
	while (<$fh>) {
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

sub read_runtable() {
	my %runtable;

	open my $fh, '<', 'runtable.txt' or die $!;
	while (<$fh>) {
		chomp;
		my ($date, $group, $state) = split /\t/, $_;
		$runtable{$date}{$group} = $state;
	}
	close $fh;

	return \%runtable;
}

sub force_utf8($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? encode_utf8($enc->decode($str)) : $str;
}

sub addnor($) {
	my $orgstr=$_[0];
	$orgstr=~ s/　//g;
	$orgstr=~ s/ //g;
	$orgstr=~ s/が//g;
	$orgstr=~ s/ケ//g;
	$orgstr=~ s/ヶ//g;
	$orgstr=~ s/の//g;
	$orgstr=~ s/ノ//g;
	return $orgstr;
}

sub gettimetablever{
	open (VREAD,"$Bin/timetable.txt");
	while(<VREAD>) {
		chomp;
		my ($firm,$ver)=split(/\t/,$_);
		if($firm eq "V") {
			close(VREAD);
			return $ver;
		}
	}
	close(VREAD);
	return '--';
}

sub getareatablever{
	open (VREAD,"$Bin/all.all");
	while(<VREAD>) {
		chomp;
		my ($field,$ver)=split(/\t/,$_);
		if($field eq "version") {
			close(VREAD);
			return $ver;
		}
	}
	close(VREAD);
	return '--';
}

my $query=new CGI;
my $comm=$query->param('comm');
my $getcity=force_utf8($query->param('city'));
my $titlename=$getcity;
$getcity = addnor $getcity;
$getcity=~ s/0/０/g;
$getcity=~ s/1/１/g;
$getcity=~ s/2/２/g;
$getcity=~ s/3/３/g;
$getcity=~ s/4/４/g;
$getcity=~ s/5/５/g;
$getcity=~ s/6/６/g;
$getcity=~ s/7/７/g;
$getcity=~ s/8/８/g;
$getcity=~ s/9/９/g;
my $getgroup=int($query->param('gid'));
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}
my $ver='1.14alpha';
my $auth='mnakajim';

if ($comm=~ m/ver/gi) {
	my $timetable=&gettimetablever();
	my $areatable=&getareatablever();
	print "Content-type: text/plain\n\narea.cgi : $ver($auth)\n";
	print "timetable.txt : $timetable\n";
	print "areatable.txt : $areatable\n";
	exit;
}


$titlename=~ s/[;\"\'\$\@\%\(\)]//g;

open (READ,"$Bin/all.all");

my @results;
my $count=0;

my $runtable = read_runtable;
my $timetable = read_timetable;
my @dates = map {date_str(time + DAY_SECONDS * $_)} 0 .. 2;

while (<READ>) {
	chomp;
	my ($area1,$area2,$area3,$num,$grp)=split (/\t/,$_);
	my $firm = 'T';  # XXX 東電。現状の実装では固定。
	my $areaorg="$area1$area2$area3";
	$areaorg = addnor $areaorg;

	if ($getgroup) {
		next unless $areaorg=~ m/$getcity/ and $num eq $getgroup;
	} else {
		next unless $areaorg=~ m/$getcity/;
	}

	my $bgcolor='FFEEFF';
	if ($count % 2 ==0) {
		$bgcolor='EEFFFF';
	}


	my @hours = map {
		my $hours = $timetable->{$firm}{$_}{$num};
		my $run_str = $runtable->{$_}{"$num\-$grp"} || '-';
		my $hours_str = $hours ? join(', ', @$hours) : '-';
		decode_utf8 "$hours_str($run_str)";
	} @dates;

	push @results, {
		bgcolor => $bgcolor,
		tdfk => (decode_utf8 $area1), 
		shiku => (decode_utf8 $area2), 
		machiaza => (decode_utf8 $area3),
		hours => \@hours,
		num => $num, grp => $grp,
	};
	++$count;
}

my $error_message;
if (!$count) {
	$error_message = "計画停電のないエリアです。";
}
if ($count>400) {
	$error_message = "該当地域が多すぎです。詳細の地域名を入力してください。";
}

my $mtf = Text::MicroTemplate::File->new;
print "Content-Type: text/html;charset=utf-8\n\n";
print $mtf->render_file(
	"$Bin/area.html", 
	decode_utf8($titlename), \@dates, \@results, decode_utf8($error_message)
);
