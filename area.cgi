#!/usr/bin/perl

BEGIN {
	$conv_start = (times)[0];
}
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

#2011/03/16|12:20-16:00|15:20-19:00|18:20-22:00|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30
#2011/03/17|09:20-13:00|16:50-20:30|12:20-16:00|15:20-19:00|18:20-22:00|06:20-10:00, 13:50-17:30

$gto=<<FIN;
2011/03/18|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30|12:20-16:00|15:20-19:00|18:20-22:00
2011/03/19|18:20-22:00|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30|12:20-16:00|15:20-19:00
2011/03/20|15:20-19:00|18:20-22:00|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30|12:20-16:00
2011/03/21|12:20-16:00|15:20-19:00|18:20-22:00|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30
2011/03/22|09:20-13:00, 16:50-20:30|12:20-16:00|15:20-19:00|18:20-22:00|06:20-10:00, 13:50-17:30
2011/03/23|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30|12:20-16:00|15:20-19:00|18:20-22:00
2011/03/24|18:20-22:00|06:20-10:00, 13:50-17:30|09:20-13:00, 16:50-20:30|12:20-16:00|15:20-19:00
FIN

# 東北電力
$gth=<<FIN;
2011/03/16|09:00-12:00|09:00-12:00|17:00-20:00|17:00-20:00|　|　|　|　
2011/03/17|　　|　|　|09:00-12:00|09:00-12:00|17:00-20:00|17:00-20:00
2011/03/18|09:00-12:00|09:00-12:00|17:00-20:00|17:00-20:00|　|　|　|　
2011/03/19|　|　|　|　|　|　|　|　
2011/03/20|　|　|　|　|　|　|　|　
2011/03/21|　|　|　|　|　|　|　|　
2011/03/22|　|　|　|　|　|　|　|　
2011/03/23|　|　|　|　|　|　|　|　
2011/03/24|　|　|　|　|　|　|　|　
FIN

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

# 日付取得
for($i=0; $i<5; $i++) {
	$date[$i]=&date("Y/m/d",,time+86400*$i);
	$mon[$i]=&date("n",,time+86400*$i);
	$mday[$i] = &date("j",,time+86400*$i);
}

# タイムテーブル解析

foreach $line(split(/\n/,$gto)) {
	($p[0],$p[1],$p[2],$p[3],$p[4],$p[5],$p[6],$p[7],$p[8])=split(/\|/,$line);
	for($i=0; $i<5; $i++) {
		if($p[0] eq $date[$i]) {
			for($grp=1; $grp<=8; $grp++) {
				$gto{"$date[$i]_$grp"}=$p[$grp];
			}
		}
	}
}

foreach $line(split(/\n/,$gth)) {
	($p[0],$p[1],$p[2],$p[3],$p[4],$p[5],$p[6],$p[7],$p[8])=split(/\|/,$line);
	for($i=0; $i<5; $i++) {
		if($p[0] eq $date[$i]) {
			for($grp=1; $grp<=8; $grp++) {
				$gth{"$date[$i]_$grp"}=$p[$grp];
EOM
			}
		}
	}
}

# 携帯かどうか？

$mobileflg=4;
$mobileflg=3 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE/);

$buf=<<FIN;
<table border=1><tr bgcolor=#C0C0C0><th>地域</th>
FIN
if($mobileflg eq 3) {
	for($i=0; $i<$mobileflg; $i++) {
		$buf.=<<FIN;
	<th>$mday[$i]日停電時間</th>
FIN
	}
} else {
	for($i=0; $i<$mobileflg; $i++) {
		$buf.=<<FIN;
	<th>$mon[$i]月$mday[$i]日停電時間</th>
FIN
	}
}

$buf.=<<FIN;
<th>グループ</th></tr></tr>
FIN

$head=$buf;
$buf='';

open (READ,"all.all");

$count=0;

if ($zip2 eq "0000") {
	$buf="<tr><td colspan=5>郵便番号末尾４桁 0000 では検索できません。</td></tr>";
} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
	$buf="<tr><td colspan=5>郵便番号が正確に入力されていないようです。</td></tr>";
} else {
	while (<READ>) {
		chomp;
		($area1,$area2,$area3,$num)=split (/\t/,$_);
		$areaorg="$area1$area2$area3";
		$areaorg=~ s/ //g;

		foreach(@tokyo_denryoku_list) {
			if($area1 eq $_) {
				%g=%gto;
				last;
			}
		}
		foreach(@tohoku_denryoku_list) {
			if($area1 eq $_) {
				%g=%gth;
				last;
			}
		}

		if ($count % 2 ==0) {
			$bgcolor='EEFFFF';
		} else {
			$bgcolor='FFEEFF';
		}

		if ($getgroup) {
			if ($areaorg=~ m/$getcity/ and $num eq $getgroup) {
				$buf.=<<FIN;
<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td>
FIN
				for($i=0; $i<$mobileflg; $i++) {
					$buf.=<<FIN;
<td>$g{"$date[$i]_$num"}</td>
FIN
				}
				$buf.=<<FIN;
<td>第$numグループ</td></tr>
FIN
				++$count;
			}
		} else {
			if ($areaorg=~ m/$getcity/) {
				$buf.=<<FIN;
<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td></td>
FIN
				for($i=0; $i<$mobileflg; $i++) {
					$buf.=<<FIN;
<td>$g{"$date[$i]_$num"}</td>
FIN
				}
				$buf.=<<FIN;
<td>第$numグループ</td></tr>
FIN
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
}

if($zip ne '') {
	$areas="〒$zip1-$zip2";
} else {
	$areas="$getcity";
}

print <<FIN;
Content-type: text/html;charset=utf-8
Cache-Control: max-age=0
Expires: Mon, 26, Jul 1997 05:00:00 GMT

<html><head>
<title>$areasの計画停電予定</title></head>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。
$head
$buf
</table><a href=./>戻る</a><hr>
FIN

printf("Powered by Perl $] HTML convert time to %.3f sec.",
		((times)[0] - $::_conv_start));

print <<FIN;
</body>
</html>
FIN

# 面倒なのでpyukiwikiから移植ｗ

sub date {
	my ($format, $tm, $gmtime) = @_;
	my %weekday;
	my %ampm;

	# yday:0-365 $isdst Summertime:1/not:0
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = 
		$gmtime ne '' && @_ > 2
			? ($tm+0 > 0 ? gmtime($tm) : gmtime(time))
			: ($tm+0 > 0 ? localtime($tm) : localtime(time));

	$year += 1900;
	my $hr12=$hour=>12 ? $hour-12:$hour;
	# year
	$format =~ s/Y/$year/ge;	# Y:4char ex)1999 or 2003

	# month
	$mon++;									# mon is 0 to 11 add 1
	$format =~ s/n/$mon/ge;					# n:1-12
	$mon = "0" . $mon if ($mon < 10);
	$format =~ s/m/$mon/ge;					# m:01-12

	# day
	$format =~ s/j/$mday/ge;				# j:1-31
	$mday = "0" . $mday if ($mday < 10);
	$format =~ s/d/$mday/ge;				# d:01-31
	return $format;
}

