#!/usr/bin/perl

use CGI;
$query=new CGI;
$getcity=$query->param('city');
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=$query->param('gid');
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}
@grp=('', '15:20-19:00', '18:20-22:00', '06:20-10:00', '09:20-13:00', '12:20-16:00');
@g16=('', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30');
@g17=('', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30');
@g18=('', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00');


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
			$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td><td>$g16[$num]</td><td>$g17[$num]</td><td>$g18[$num]</td><td>第$numグループ</td></tr>\n";
			++$count;
		}
	} else {
		if ($areaorg=~ m/$getcity/) {
			$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td></td><td>$g16[$num]</td><td>$g17[$num]</td><td>$g18[$num]</td><td>第$numグループ</td></tr>\n";
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
Content-type: text/html;charset=utf-8\n\n<title>検索結果</title>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。
<table border=1><tr bgcolor=#C0C0C0><th>地域</th><th>16日停電時間</th><th>17日停電時間</th><th>18日停電時間</th><th>グループ</th></tr>
$buf
</table><a href=./>戻る</a>
FIN
