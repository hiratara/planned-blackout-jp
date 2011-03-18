#!/usr/bin/perl

require 'gval.pl';

use Jcode;
use CGI;
$query=new CGI;
$comm=$query->param('comm');
$getcity=$query->param('city');
$getcity=Jcode->new($getcity)->utf8;
$titlename=$getcity;
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=int($query->param('gid'));
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}
$ver='1.121';
$auth='mnakajim';

if ($comm=~ m/ver/gi) {
	print "Content-type: text/plain\n\n$ver($auth)\n";
	exit;
}


$titlename=~ s/[;\"\'\$\@\%\(\)]//g;

open (READ,"all.all");

$buf='';
$count=0;

while (<READ>) {
	chomp;
	($area1,$area2,$area3,$num)=split (/\t/,$_);
	$areaorg="$area1$area2$area3";
	$areaorg=~ s/ //g;

	if ($count % 2 ==0) {
		$bgcolor='EEFFFF';
	} else {
		$bgcolor='FFEEFF';
	}

	if ($getgroup) {
		if ($areaorg=~ m/$getcity/ and $num eq $getgroup) {
			$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td><td>$day1[$num]</td><td>$day2[$num]</td><td>$day3[$num]</td><td>第$numグループ</td></tr>\n";
			++$count;
		}
	} else {
		if ($areaorg=~ m/$getcity/) {
			$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td></td><td>$day1[$num]</td><td>$day2[$num]</td><td>$day3[$num]</td><td>第$numグループ</td></tr>\n";
			++$count;
		}
	}
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
このページをブックマークしておくと、ブックマーク呼び出しだけで地域名の入力が不要です。
<table border=1><tr bgcolor=#C0C0C0><th>地域</th><th>$day1[0]日停電時間</th><th>$day2[0]日停電時間</th><th>$day3[0]日停電時間</th><th>グループ</th></tr>
$buf
</table><a href=./>戻る</a>
FIN
