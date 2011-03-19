#!/usr/bin/perl

BEGIN {
	$conv_start = (times)[0];
}

use CGI;
use Encode qw(from_to);

require 'gval.pl';

$query=new CGI;
$getcity=$query->param('city');
$tmp=$getcity;
$enc=&getcode(\$tmp);
if($enc ne 'utf8' && $enc ne '') {
	from_to($getcity,$enc,'utf8');
}
$zip1=$query->param('zip1');
$zip2=$query->param('zip2');
$out=$query->param('out');
$comm=$query->param('comm');
$zip=$zip1 . $zip2;
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=$query->param('gid');
if ($getgroup>8 || $getgroup<=0) {
	$getgroup=0;
}

$getcity=~s/ケ/ヶ/g;

if($comm eq 'ver') {
	open(R,"index.html");
	foreach(<R>) {
		if(/^V\.(.*)/) {
			$VER=$1;
			print <<FIN;
Content-type: text/plain; charset=utf-8

$VER
FIN
		}
	}
	close(R);
	exit;
}

if($zip ne '') {
	open (ZIP,"yubin.csv");
	while(<ZIP>) {
		chomp;
		push(@ZIP,$_);
	}
	close(ZIP);
	if($zip2 ne "0000") {
		foreach(@ZIP) {
			s/ケ/ヶ/g;
			($ziptmp,$kanji1,$kanji2,$kanji3)=split(/\t/,$_);
			if($ziptmp eq $zip) {
				open (READ,"all.all");
				while (<READ>) {
					s/ケ/ヶ/g;
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
$mobileflg=2 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE/);

if($out eq 'rss') {
	&getbasehref;
	$buf='';
	$rssdate=&date("Y-m-dTH:i:s+9:00");

	open (READ,"all.all");

	$count=0;

	if ($zip2 eq "0000") {
		$buf="郵便番号末尾４桁 0000 では検索できません。";
	} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
		$buf="郵便番号が正確に入力されていないようです。";
	} else {
		while (<READ>) {
			s/ケ/ヶ/g;
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


			if ($getgroup) {
				if ($areaorg=~ m/$getcity/ and $num eq $getgroup) {
					for($i=0; $i<$mobileflg; $i++) {
						$_getcity=&encode($getcity);
						$xml=<<FIN;
<item rdf:about="$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup">
<title>【$mon[$i]月$mday[$i]日】$arrea1$area2$area3(グループ$num)の計画停電情報です。</title>
<link>$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<description>$g{"$date[$i]_$num"}です。</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
						$XML{"$date[$i]"}.=$xml;
					}
					++$count;
				}
			} else {
				if ($areaorg=~ m/$getcity/) {
					for($i=0; $i<$mobileflg; $i++) {
						$_getcity=&encode($getcity);
						$xml=<<FIN;
<item rdf:about="$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup">
<title>【$mon[$i]月$mday[$i]日】$arrea1$area2$area3(グループ$num)の計画停電情報です。</title>
<link>$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<description>$g{"$date[$i]_$num"}です。</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
						$XML{"$date[$i]"}.=$xml;
					}
					++$count;
				}
			}
		}
		if (!$count) {
			$buf="計画停電のないエリアです。";
		}
		if ($count>400) {
			$buf="該当地域が多すぎです。詳細の地域名を入力してください。";
		}
	}

	if($zip ne '') {
		$areas="〒$zip1-$zip2";
	} else {
		$areas="$getcity";
	}
	$areas=~ s/[;\"\'\$\@\%\(\)]//g;	# by @mnakajim

	print <<FIN;
Content-type: text/xml;charset=utf-8
Cache-Control: max-age=0
Expires: Mon, 26, Jul 1997 05:00:00 GMT

<?xml version="1.0" encoding="UTF-8" ?>

<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns="http://purl.org/rss/1.0/"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
>
FIN
	if($buf ne '') {
		print <<FIN;
<channel rdf:about="$::basehost/index.html">
 <title>$areasの計画停電予定</title>
 <link>$::basehost/index.html</link>
</channel>
<item rdf:about="$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup">
<title>$buf</title>
<link>$::basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<dc:date>$rssdate</dc:date>
</item>
FIN
	} else {
		print <<FIN;
<channel rdf:about="$::basehost$basepath">
<title>$areasの計画停電予定</title>
<link>$::basehost$basepath</link>
</channel>
FIN
		for($i=0; $i<$mobileflg; $i++) {
			print $XML{"$date[$i]"};
		}
	}
	print <<FIN;
</rdf:RDF>
FIN
	exit;
}

$buf=<<FIN;
<table border=1><tr bgcolor=#C0C0C0><th>地域</th>
FIN
if($mobileflg eq 2) {
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
		s/ケ/ヶ/g;
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
$areas=~ s/[;\"\'\$\@\%\(\)]//g;	# by @mnakajim

print <<FIN;
Content-type: text/html;charset=utf-8
Cache-Control: max-age=0
Expires: Mon, 26, Jul 1997 05:00:00 GMT

<html><head>
<title>$areasの計画停電予定</title></head>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<BR>
このページをブックマークしておくと、ブックマーク呼び出しだけで地域名の入力が不要です。 <BR>
$head
$buf
</table>
[<a href=./>戻る</a>] 
[<a href="area.cgi?city=$getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup&out=rss">RSS</a>]
<hr>
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

	# hour
	$hour = "0" . $hour if ($hour < 10);
	$format =~ s/H/$hour/ge;				# H:00-23

	# minutes
	$min = "0" . $min if ($min < 10);
	$format =~ s/i/$min/ge;					# i:00-59

	# second
	$sec = "0" . $sec if ($sec < 10);
	$format =~ s/s/$sec/ge;					# s:00-59

	return $format;
}

# これも面倒だからpyukiwikiから移植
sub getbasehref {
	# Thanks moriyoshi koizumi.
	$::basehost = "$ENV{'HTTP_HOST'}";
	$::basehost = 'http://' . $::basehost;
	# Special Thanks to gyo
	$::basehost .= ":$ENV{'SERVER_PORT'}"
		if ($ENV{'SERVER_PORT'} ne '80' && $::basehost !~ /:\d/);
	# URLの生成
	my $uri;
	my $req=$ENV{REQUEST_URI};
	$req=~s/\?.*//g;
	if($req ne '') {
		if($req eq $ENV{SCRIPT_NAME}) {
			$uri= $ENV{'SCRIPT_NAME'};
		} else {
			for(my $i=0; $i<length($ENV{SCRIPT_NAME}); $i++) {
				if(substr($ENV{SCRIPT_NAME},$i,1) eq substr($req,$i,1)) {
					$uri.=substr($ENV{SCRIPT_NAME},$i,1);
				} else {
					last;
				}
			}
		}
	} else {
		$uri .= $ENV{'SCRIPT_NAME'};
	}
	$::basehref=$::basehost . $uri;
	$::basepath=$uri;
	$::basepath=~s/\/[^\/]*$//g;
	$::basepath="/" if($::basepath eq '');
	$::script=$uri if($::script eq '');
}

# これも面倒だからpyukiwikiから移植
sub encode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}


# jcode.pl & Jcode.pm より移植

sub init {
    $re_bin  = '[\000-\006\177\377]';

    $re_jis0208_1978 = '\e\$\@';
    $re_jis0208_1983 = '\e\$B';
    $re_jis0208_1990 = '\e&\@\e\$B';
    $re_jis0208 = "$re_jis0208_1978|$re_jis0208_1983|$re_jis0208_1990";
    $re_jis0212 = '\e\$\(D';
    $re_jp      = "$re_jis0208|$re_jis0212";
    $re_asc     = '\e\([BJ]';
    $re_kana    = '\e\(I';

    $esc_0208 = "\e\$B";
    $esc_0212 = "\e\$(D";
    $esc_asc  = "\e(B";
    $esc_kana = "\e(I";

    $re_sjis_c    = '[\201-\237\340-\374][\100-\176\200-\374]';
    $re_sjis_kana = '[\241-\337]';

    $re_euc_c    = '[\241-\376][\241-\376]';
    $re_euc_kana = '\216[\241-\337]';
    $re_euc_0212 = '\217[\241-\376][\241-\376]';

    $re_utf8 = '[\xc0-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf][\x80-\xbf]';

    # Use `geta' for undefined character code
    $undef_sjis = "\x81\xac";

    $cache = 1;

}

sub getcode {
	&init;
    local(*s) = @_;
    local($matched, $code);

    if ($s !~ /[\e\200-\377]/) {	# not Japanese
	$matched = 0;
	$code = undef;
    }					# 'jis'
    elsif ($s =~ /$re_jp|$re_asc|$re_kana/o) {
	$matched = 1;
	$code = 'jis';
    }
    elsif ($s =~ /$re_bin/o) {		# 'binary'
	$matched = 0;
	$code = 'binary';
    }
    else {				# should be 'euc' or 'sjis' or 'utf8'
	local($sjis, $euc, $utf8) = (0, 0, 0);

	while ($s =~ /(($re_sjis_c)+)/go) {
	    $sjis += length($1);
	}
	while ($s =~ /(($re_euc_c|$re_euc_kana|$re_euc_0212)+)/go) {
	    $euc  += length($1);
	}
    while ($s =~ /(($re_utf8)+)/go) {
		$utf8 += length($1);
	}
	$code = 
	    ($euc > $sjis and $euc > $utf8) ? 'euc-jp' :
		($sjis > $euc and $sjis > $utf8) ? 'shiftjis' :
		    ($utf8 > $euc and $utf8 > $sjis) ? 'utf8' : undef;
    }
    $code;
}
