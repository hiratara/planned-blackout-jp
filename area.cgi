#!/usr/bin/perl

BEGIN {
	$conv_start = (times)[0];
}

use CGI;
use Encode qw/decode encode_utf8 from_to/;
use Encode::Guess;
require 'gval.pl';

$query=new CGI;
$getcity=$query->param('city');
$getcity=force_utf8($query->param('city'));

$zip=$query->param('zip');
$zip=~s/\-//g;
if($zip eq '') {
	$zip1=$query->param('zip1');
	$zip2=$query->param('zip2');
	$zip=$zip1 . $zip2;
}
if($zip ne '') {
	$zip1=substr($zip,0,3);
	$zip2=substr($zip,2,4);
}
$out=$query->param('out');
$comm=$query->param('comm');
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=$query->param('gid');
if ($getgroup>8 || $getgroup<=0) {
	$getgroup=0;
}

$getcity=~s/ケ/ヶ/g;
$getcity=~s/の/ノ/g;

&tr(\$getcity,'[0-9]', '[０-９]');

if($comm eq 'ver') {
	print <<FIN;
Content-type: text/plain; charset=utf-8

FIN

	open(R,"index.cgi");
	foreach(<R>) {
		if(/\$VER\=\"V\.(.+)\"\;/) {
			$VER=$1;
			print "$VER";
			close(R);
			exit;
		}
	}
	close(R);
	print "What version ? or older";
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
			s/の/ノ/g;
			($ziptmp,$kanji1,$kanji2,$kanji3)=split(/\t/,$_);
			if($ziptmp eq $zip) {
				open (READ,"all.all");
				while (<READ>) {
					s/ケ/ヶ/g;
					s/の/ノ/g;
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
			s/の/ノ/g;
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
		s/の/ノ/g;
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
$debug
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

# by hiratara

sub force_utf8($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? encode_utf8($enc->decode($str)) : $str;
}

# from jcode.pl

;#
;# TR function for 2-byte code
;#
sub tr {
    # $prev_from, $prev_to, %table are persistent variables
    local(*s, $from, $to, $opt) = @_;
    local(@from, @to);
    local($n) = (0, 0);
    
	from_to($s,'utf8','euc-jp');
	from_to($from, 'utf8', 'euc-jp');
	from_to($to, 'utf8', 'euc-jp');

	&_maketable;

    $s =~ s/([\200-\377][\000-\377]|[\000-\377])/
	defined($table{$1}) && ++$n ? $table{$1} : $1
    /ge;

	from_to($s,'euc-jp','utf8');

    $n;
}

sub _maketable {
    local($ascii) = '(\\\\[\\-\\\\]|[\0-\133\135-\177])';

    grep(s/(([\200-\377])[\200-\377]-\2[\200-\377])/&_expnd2($1)/ge,
	 $from, $to);
    grep(s/($ascii-$ascii)/&_expnd1($1)/geo,
	 $from, $to);

    @to   = $to   =~ /[\200-\377][\000-\377]|[\000-\377]/g;
    @from = $from =~ /[\200-\377][\000-\377]|[\000-\377]/g;
    push(@to, ($opt =~ /d/ ? '' : $to[$#to]) x (@from - @to)) if @to < @from;
    @table{@from} = @to;
}

sub _expnd1 {
    local($s) = @_;
    $s =~ s/\\(.)/$1/g;
    local($c1, $c2) = unpack('CxC', $s);
    if ($c1 <= $c2) {
	for ($s = ''; $c1 <= $c2; $c1++) {
	    $s .= pack('C', $c1);
	}
    }
    $s;
}

sub _expnd2 {
    local($s) = @_;
    local($c1, $c2, $c3, $c4) = unpack('CCxCC', $s);
    if ($c1 == $c3 && $c2 <= $c4) {
	for ($s = ''; $c2 <= $c4; $c2++) {
	    $s .= pack('CC', $c1, $c2);
	}
    }
    $s;
}
