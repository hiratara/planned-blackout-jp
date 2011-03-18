#!/usr/bin/perl

use CGI;
use Jcode;
$query=new CGI;
$getcity=$query->param('city');
$getcity=Jcode->new($getcity)->utf8;
$zip1=$query->param('zip1');
$zip2=$query->param('zip2');
$zip=$zip1 . $zip2;
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=$query->param('gid');
if ($getgroup>8 || $getgroup<=0) {
	$getgroup=0;
}

# 東京電力
@gto16=('', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30');
@gto17=('', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30');
@gto18=('', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00');

# 東北電力
@gth16=('　', '09:00-12:00', '09:00-12:00', '17:00-20:00', '17:00-20:00','　','　','　','　');
@gth17=('　', '　', '　', '　', '　', '09:00-12:00', '09:00-12:00', '17:00-20:00', '17:00-20:00');
@gth18=('　', '09:00-12:00', '09:00-12:00', '17:00-20:00', '17:00-20:00','　','　','　','　');

# 東京電力リスト
@tokyo_denryoku_list=("茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","山梨県","静岡県");

# 東北電力リスト
@tohoku_denryoku_list=("青森県","秋田県","岩手県","宮城県","山形県","福島県","新潟県");

if($zip ne '') {
	open (ZIP,"yubin.csv");
	while(<ZIP>) {
		chomp;
		push(@ZIP,$_);
	}
	close(ZIP);
	if($zip2 ne "0000") {
		foreach(@ZIP) {
			($ziptmp,$kana1,$kana2,$kana3,$kanji1,$kanji2,$kanji3)=split(/\t/,$_);
			if($ziptmp eq $zip) {
				open (READ,"all.all");
				while (<READ>) {
					chomp;
					($area1,$area2,$area3,$num)=split (/\t/,$_);
					if($kanji1 eq $area1 && $kanji2 eq $area2 && ($area3 =~/$kanji3/ || $kanji3 =~/$area3/)) {
						$getcity="$area1$area2$area3";
						last;
					}
				}
				close(READ);
			}
		}
	}
}

open (READ,"all.all");

$buf='';
$count=0;

while (<READ>) {
	chomp;
	($area1,$area2,$area3,$num)=split (/\t/,$_);
	$areaorg="$area1$area2$area3";
	$areaorg=~ s/ //g;

# 日付変更時に変更必須
	foreach(@tokyo_denryoku_list) {
		if($area1 eq $_) {
			@g16=@gto16;
			@g17=@gto17;
			@g18=@gto18;
		}
	}
	foreach(@tohoku_denryoku_list) {
		if($area1 eq $_) {
			@g16=@gth16;
			@g17=@gth17;
			@g18=@gth18;
		}
	}

	if ($count % 2 ==0) {
		$bgcolor='EEFFFF';
	} else {
		$bgcolor='FFEEFF';
	}

	if ($getgroup) {
		foreach $_getcity(split(/\t/,$getcity)) {
			if ($areaorg=~ m/$_getcity/ and $num eq $getgroup) {
				$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td><td>$g16[$num]</td><td>$g17[$num]</td><td>$g18[$num]</td><td>第$numグループ</td></tr>\n";
				++$count;
			}
		}
	} else {
		foreach $_getcity(split(/\t/,$getcity)) {
			if ($areaorg=~ m/$_getcity/) {
				$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td></td><td>$g16[$num]</td><td>$g17[$num]</td><td>$g18[$num]</td><td>第$numグループ</td></tr>\n";
				++$count;
			}
		}
	}
}

if (!$count) {
	$buf="<tr><td colspan=5>計画停電のないエリアです。</td></tr>";
}
if ($zip2 eq "0000") {
	$buf="<tr><td colspan=5>郵便番号末尾４桁 0000 では検索できません。</td></tr>";
}
if ($count>400) {
	$buf="<tr><td colspan=5>該当地域が多すぎです。詳細の地域名を入力してください。</td></tr>";
}

if (($zip1 ne '' && $zip2 eq '') || ($zip1 eq '' && $zip2 ne '')) {
	$buf="<tr><td colspan=5>郵便番号が正確に入力されていないようです。</td></tr>";
}

if($zip ne '') {
	$areas=" - 〒$zip1-$zip2";
} else {
	$areas=" - $getcity";
}

print <<FIN;
Content-type: text/html;charset=utf-8
Cache-Control: max-age=0
Expires: Mon, 26, Jul 1997 05:00:00 GMT

<title>計画停電時間検索検索結果$areas</title>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。
<table border=1><tr bgcolor=#C0C0C0><th>地域</th><th>16日停電時間</th><th>17日停電時間</th><th>18日停電時間</th><th>グループ</th></tr>
$buf
</table><a href=./>戻る</a>
FIN
