#!/usr/bin/perl
use strict;
use warnings;
use Encode qw/decode encode_utf8/;
use Encode::Guess;
use CGI;
use constant DAY_SECONDS => 24 * 60 * 60;

sub date_str($) {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

sub read_timetable() {
	my %timetable;

	open my $fh, '<', 'timetable.txt' or die $!;
	while (<$fh>) {
		my ($date, $group, @hours) = split /\t/, $_;
		$timetable{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

my $query=new CGI;
my $comm=$query->param('comm');
my $getcity=force_utf8($query->param('city'));
my $titlename=$getcity;
$getcity=~ s/ //g;
$getcity=~ s/　//g;
my $getgroup=int($query->param('gid'));
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}
my $ver='1.122';
my $auth='mnakajim';

if ($comm=~ m/ver/gi) {
	print "Content-type: text/plain\n\n$ver($auth)\n";
	exit;
}


$titlename=~ s/[;\"\'\$\@\%\(\)]//g;

open (READ,"all.all");

my $buf='';
my $count=0;

my $timetable = read_timetable;
my @dates = map {date_str(time + DAY_SECONDS * $_)} 0 .. 2;

while (<READ>) {
	chomp;
	my ($area1,$area2,$area3,$num)=split (/\t/,$_);
	my $areaorg="$area1$area2$area3";
	$areaorg=~ s/ //g;

	my $bgcolor;
	if ($count % 2 ==0) {
		$bgcolor='EEFFFF';
	} else {
		$bgcolor='FFEEFF';
	}

	if ($getgroup) {
		next unless $areaorg=~ m/$getcity/ and $num eq $getgroup;
	} else {
		next unless $areaorg=~ m/$getcity/;
	}

	my @hours = map {
		my $hours = $timetable->{$_}{$num};
		$hours ? join(', ', @$hours) : '-';
	} @dates;
	$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td>" . 
	      join('', map {"<td>$_</td>"} @hours) . 
	      "<td>第$numグループ</td></tr>\n";
	++$count;
}

if (!$count) {
	$buf="<tr><td colspan=5>計画停電のないエリアです。</td></tr>";
}
if ($count>400) {
	$buf="<tr><td colspan=5>該当地域が多すぎです。詳細の地域名を入力してください。</td></tr>";
}
print <<FIN;
Content-type: text/html;charset=utf-8\n\n<title>$titlenameの計画停電予定</title>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<BR>
このページをブックマークしておくと、次回からは地域名の入力が不要です。
<table border=1><tr bgcolor=#C0C0C0><th>地域</th>${\
  join('', map {"<th>$_停電時間</th>"} @dates)
}<th>グループ</th></tr>
$buf
</table><a href=./>戻る</a>
FIN

sub force_utf8($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? encode_utf8($enc->decode($str)) : $str;
}
