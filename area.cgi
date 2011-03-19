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
<body background="obi.jpg">
V.1.121
<br>
<table width="100%" bgcolor=#FFEFD5><tr><td>
<img src="title.jpg" height="150px">
</td>
<td align="right">
	<table><tr>
	<td align="center">　<a href="http://182.48.61.190/power/touhoku.html"><img src="tohoku.gif" height="40px"></a>
		<br />　東北電力
	</td>
	<td align="center">　<a href="develop.html"><img src="develop.gif" height="40px"></a>
		<br />　開発情報
	</td>
	</table>
</td>
</tr>
</table>
<br />
<br />
<table width = 100%>
<tr>
<td>
<table width="100%">
<tr>
<td valign="middle" height="300px">
<div align="center">
<img src="kekka.jpg" width="250px"><br /><br />

$count 件が見つかりました。<br />
<br />
<div align="left">
同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実施されます。<BR>
このページをブックマーク（お気に入り）しておくと、次回から簡単に閲覧できます。
<br />
<br />
<div align="center"><a href=./>検索条件を変更する</a></div>
<br />
<br />
<table border=1><tr bgcolor=#C0C0C0><th>地域</th><th>$day1[0]日停電時間</th><th>$day2[0]日停電時間</th><th>$day3[0]日停電時間</th><th>グループ</th></tr>
$buf
</div>
</table>
<br />
<br />
<div align="center"><a href=./>検索条件を変更する</a></div>
</td>
</tr>
<tr>
<td>
<b>データ更新:</b>　2011/3/18 23:55　[<a href="http://bizoole.com/power/history/datahistory.html">詳細</a>]
<br />
<b>エンジン更新:</b>　2011/3/19 00:25　[<a href="http://bizoole.com/power/history/">詳細</a>]
</p>
問い合わせは、<a href="http://twitter.com/mnakajim">twitter (@mnakajim)</a>へ<BR><br>
<div align="right">
copyright(c) system:<a href=http://twitter.com/mnakajim/>中島昌彦</a> and icons:<a href=http://twitter.com/watanabe_haruna/>渡邉春菜</a>
</div>
</td>
</tr>
</table>
</td>
<td valign="top">
<!--twitter用スクリプト http://www.twitstat.us/-->
<a href="http://twitter.com/#!/search/%23jishin_power" target=_blank>計画停電ハッシュタグ</a>
<div class="twitstatus_badge_container" id="twitstat_badge_871"></div>
<script type="text/javascript" src="http://twitstat.us/twitstat.us-min.js"></script>
<script type="text/javascript">
twitstat.badge.init({
    badge_container: "twitstat_badge_871",
    title: "　",
    keywords: "#jishin_power",
    max: 7,
    border_color: "#434343",
    header_background: "#434343",
    header_font_color: "#ffffff",
    content_background_color: "#e1e1e1",
    content_font_color: "#333333",
    link_color: "#307ace",
    width: 350
});
</script>
<!--ここまでtwitter用スクリプト -->


</td>
</tr>
</table>
</body>

</html>

FIN
