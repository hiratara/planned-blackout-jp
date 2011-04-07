#!/usr/bin/perl

BEGIN {
	$conv_start = (times)[0];
}

use CGI;
use Encode qw/decode encode_utf8 from_to/;
use Encode::Guess;

$query=new CGI;
$getcity=$query->param('city');
$getcity=force_utf8($query->param('city'));
$zip=$query->param('zip');
$mode=$query->param('m');
$englishflg=0;
$englishflg=1 if($mode eq 'e');
$mflg=1 if($mode eq 'm');

$zip=~s/\-//g;
if($zip eq '') {
	$zip1=$query->param('zip1');
	$zip2=$query->param('zip2');
	$zip=$zip1 . $zip2;
}
if($zip=~/(\d\d\d)(\d\d\d\d)/) {
	$zip1=$1;
	$zip2=$2;
}
$out=$query->param('out');
$comm=$query->param('comm');
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getgroup=$query->param('gid');
if ($getgroup>8 || $getgroup<=0) {
	$getgroup=0;
}

if($mode eq 'qr') {
	$string=$query->param('str');
	&make_qrcode($string);
	exit;
}

# 東京電力リスト
@tokyo_denryoku_list=("茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","山梨県","静岡県");

# 東北電力リスト
@tohoku_denryoku_list=("青森県","秋田県","岩手県","宮城県","山形県","福島県","新潟県");

$getcity=~s/ケ/ヶ/g;
$getcity=~s/の/ノ/g;

$getcity=~s/0/０/g;
$getcity=~s/1/１/g;
$getcity=~s/2/２/g;
$getcity=~s/3/３/g;
$getcity=~s/4/４/g;
$getcity=~s/5/５/g;
$getcity=~s/6/６/g;
$getcity=~s/7/７/g;
$getcity=~s/8/８/g;
$getcity=~s/8/９/g;

if($englishflg) {
	$getcity=~tr/[a-z]/[A-Z/;
}
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

&getbasehref;

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
	$date[$i]=&date("Y-m-d",,time+86400*$i);
	$mon[$i]=&date("n",,time+86400*$i);
	$mday[$i] = &date("j",,time+86400*$i);
}

# 携帯かどうか？

$mobileflg=4;
$mobileflg=2 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE/) || $mflg eq 1;

my $timetable = &read_timetable;
my @dates = map {$date[$_]} 0 .. ($mobileflg - 1);

if($out eq 'rss') {
	$buf='';
	$rssdate=&date("Y-m-dTH:i:s+9:00");

	$count=0;

	if ($zip2 eq "0000") {
		if($englishflg) {
			$buf="Ending in 0000 can not find the ZIP code.";
		} else {
			$buf="郵便番号末尾４桁 0000 では検索できません。";
		}
	} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
		if($englishflg) {
			$buf="The ZIP code seems not to be input accurately.";
		} else {
			$buf="郵便番号が正確に入力されていないようです。";
		}
	} elsif($zip eq '' && $getcity eq '') {
		if($englishflg) {
			$buf="It's not input city name or ZIP code.";
		} else {
			$buf="地域名、もしくは郵便番号が入力されていません。";
		}
	} else {
		open (READ,"all.all");
		while (<READ>) {
			chomp;
			($area1,$area2,$area3,$num,$areaen1,$areaen2,$areaen3)=split (/\t/,$_);
			$areaorg="$area1$area2$area3";
			$areaorg="$area1$area2$area3$areaen1$areaen2$areaen3" if($englishflg);
			$areaorg=~ s/ //g;

			foreach(@tokyo_denryoku_list) {
				if($area1 eq $_) {
					$firm = 'T';
					last;
				}
			}
			foreach(@tohoku_denryoku_list) {
				if($area1 eq $_) {
					$firm = 'H';
					last;
				}
			}

			if ($getgroup) {
				next unless $areaorg=~ m/$getcity/ and $num eq $getgroup;
			} else {
				next unless $areaorg=~ m/$getcity/;
			}

			my @hours = map {
				my $hours = $timetable->{$firm}{$_}{$num};
				$hours ? join(', ', @$hours) : '-';
			} @dates;

			$i=0;
			foreach(@hours) {
				$_getcity=&encode($getcity);
				$hour ? join(', ', @$hours) : '-';
				if ($englishflg) {
					if(/なし/) {
						$_="none";
					}
					$xmldate[$i].=<<FIN;
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup">
<title>[$mon[$i]/$mday[$i]] @{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]} (group $num) of rolliing blackout infomation.</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<description>$_</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
				} else {
					$xmldate[$i].=<<FIN;
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup">
<title>【$mon[$i]月$mday[$i]日】$area1$area2$area3(グループ$num)の計画停電情報です。</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<description>$_です。</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
				}
				++$i;
			}
			++$count;
		}
		for($i=0; $i<$mobileflg; $i++) {
			$xml.=$xmldate[$i];
		}
		if (!$count) {
			if($englishflg) {
				$buf="Not found of rolling blakout area.";
			} else {
				$buf="計画停電のないエリアです。";
			}
		}
		if ($count>400) {
			if($englishflg) {
				$buf="There are a lot of pertinent regions. Please input a regional name of details.";
			} else {
				$buf="該当地域が多すぎです。詳細の地域名を入力してください。";
			}
		}
	}

	if($zip ne '') {
		if($englishflg) {
			$areas="ZIP:$zip1-$zip2";
		} else {
			$areas="〒$zip1-$zip2";
		}
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
	if($englishflg) {
		if($buf ne '') {
			print <<FIN;
<channel rdf:about="$basehost/index.cgi">
<title>$areas of rolling blackout schedule</title>
<link>$basehost/index.html</link>
</channel>
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup">
<title>$buf</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup</link>
<dc:date>$rssdate</dc:date>
</item>
FIN
		} else {
			print <<FIN;
<channel rdf:about="$basehost$basepath">
<title>$areas of rolling blackout schedule</title>
<link>$basehost$basepath</link>
</channel>
FIN
		}
		print $xml;
	} else {
		if($buf ne '') {
			print <<FIN;
<channel rdf:about="$basehost/index.cgi">
<title>$areasの計画停電予定</title>
<link>$basehost/index.html</link>
</channel>
<item rdf:about="$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup">
<title>$buf</title>
<link>$basehref?city=$_getcity&amp;gid=$getgroup</link>
<dc:date>$rssdate</dc:date>
</item>
FIN
		} else {
			print <<FIN;
<channel rdf:about="$basehost$basepath">
<title>$areasの計画停電予定</title>
<link>$basehost$basepath</link>
</channel>
FIN
		}
		print $xml;
	}

	print <<FIN;
</rdf:RDF>
FIN
	exit;
}

if($englishflg) {
	$buf=<<FIN;
<table border=1><tr bgcolor=#C0C0C0><th>Areas</th>
FIN
	if($mobileflg eq 2) {
		for($i=0; $i<$mobileflg; $i++) {
			$buf.=<<FIN;
<th>$mon[$i]/$mday[$i] Blackout time.</th>
FIN
		}
	} else {
		for($i=0; $i<$mobileflg; $i++) {
			$buf.=<<FIN;
<th>$mon[$i]/$mday[$i] Blackout time.</th>
FIN
		}
	}
	$buf.=<<FIN;
<th>Group No</th></tr></tr>
FIN
} else {
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
}

$head=$buf;
$buf='';

$count=0;
if ($zip2 eq "0000") {
	if($englishflg) {
		$buf="<tr><td colspan=6>Ending in 0000 can not find the ZIP code.</td></tr>";
	} else {
		$buf="<tr><td colspan=6>郵便番号末尾４桁 0000 では検索できません。</td></tr>";
	}
} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
	if($englishflg) {
		$buf="<tr><td colspan=6>The ZIP code seems not to be input accurately.</td></tr>";
	} else {
		$buf="<tr><td colspan=6>郵便番号が正確に入力されていないようです。</td></tr>";
	}
} elsif($zip eq '' && $getcity eq '') {
	if($englishflg) {
		$buf="<tr><td colspan=6>It's not input city name or ZIP code.</td></tr>";
	} else {
		$buf="<tr><td colspan=6>地域名、もしくは郵便番号が入力されていません。</td></tr>";
	}
} else {
	open (READ,"all.all");
	my $film;
	while (<READ>) {
		chomp;
		($area1,$area2,$area3,$num,$areaen1,$areaen2,$areaen3)=split (/\t/,$_);
		$areaorg="$area1$area2$area3";
		$areaorg="$area1$area2$area3$areaen1$areaen2$areaen3" if($englishflg);
		$areaorg=~ s/ //g;

		foreach(@tokyo_denryoku_list) {
			if($area1 eq $_) {
				$firm = 'T';
				last;
			}
		}
		foreach(@tohoku_denryoku_list) {
			if($area1 eq $_) {
				$firm = 'H';
				last;
			}
		}

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
			my $hours = $timetable->{$firm}{$_}{$num};
			$hours ? join(', ', @$hours) : '-';
		} @dates;

		if($englishflg) {
			$buf.="<tr bgcolor=$bgcolor><td><b>@{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]}</b></td>" . 
			      join('', map {"<td>@{[$_=~/なし/ ? 'none' : $_]}</td>"} @hours) . 
			      "<td>Group $num</td></tr>\n";

		} else {
			$buf.="<tr bgcolor=$bgcolor><td><b>$area1 $area2 $area3</b></td>" . 
			      join('', map {"<td>$_</td>"} @hours) . 
			      "<td>第$numグループ</td></tr>\n";

		}
		++$count;
	}
	if (!$count) {
		if($englishflg) {
			$buf="<tr><td colspan=6>Not found of rolling blakout area.</td></tr>";
		} else {
			$buf="<tr><td colspan=6>計画停電のないエリアです。</td></tr>";
		}
	}
	if ($count>400) {
		if($englishflg) {
			$buf="<tr><td colspan=6>There are a lot of pertinent regions. Please input a regional name of details.</td></tr>";
		} else {
			$buf="<tr><td colspan=6>該当地域が多すぎです。詳細の地域名を入力してください。</td></tr>";
		}
	}
}

if($zip ne '') {
	if($englishflg) {
		$areas="ZIP:$zip1-$zip2";
	} else {
		$areas="〒$zip1-$zip2";
	}
} else {
	$areas="$getcity";
}
$areas=~ s/[;\"\'\$\@\%\(\)]//g;	# by @mnakajim

#-- gzip圧縮

$gzip_command="gzip";

foreach(split(/:/,$ENV{PATH})) {
	if(-x "$_/$gzip_command") {
		$gzip_path="$_/$gzip_command" ;
		if(open(PIPE,"$::gzip_path --help 2>&1|")) {
			foreach(<PIPE>) {
				$forceflag="--force" if(/(\-\-force)/);
				$fastflag="--fast" if(/(\-\-fast)/);
			}
			close(PIPE);
		}
	}
}
$gzip_path="$gzip_path $fastflag $forceflag";
if ($gzip_path ne '') {
	if(($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/)) {
		if($ENV{'HTTP_ACCEPT_ENCODING'}=~/x-gzip/) {
			$gzip_header="Content-Encoding: x-gzip\n";
		} else {
			$gzip_header="Content-Encoding: gzip\n";
		}
	}
}

#-- サーバー出力
print<<END;
Content-type: text/html; charset=utf-8
Cache-Control: max-age=0
Expires: Mon, 26, Jul 1997 05:00:00 GMT
END

print "$gzip_header" if($gzip_header ne '');
print "\n";

if ($gzip_header ne '') {
	open(STDOUT,"| $gzip_path");
	binmode(STDOUT);
}

if($englishflg) {
	$html=<<FIN;
<html><head>
<title>$areas of Rolling blackout schedule</title></head>
Found $count. The schedule time is different when there are two or more registration in the same region according to the place.<BR>
When the power failure twice a day is scheduled, the power failure schedule in the latter half is executed according to the situation. <BR>
When this page is boomarked, No input of city or ZIP code.<BR>
$head
$buf
</table>
[<a href=./>Return</a>] 
FIN
} else {
	$html=<<FIN;
<html><head>
<title>$areasの計画停電予定</title></head>
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<BR>
このページをブックマークしておくと、ブックマーク呼び出しだけで地域名または郵便番号の入力が不要です。 <BR>
$head
$buf
</table>
[<a href=./>戻る</a>] 
FIN
}
if($mobileflg eq 2 || $mflg eq 1) {
	&z2h(\$html);
	$html=~s/０/0/g;
	$html=~s/１/1/g;
	$html=~s/２/2/g;
	$html=~s/３/3/g;
	$html=~s/４/4/g;
	$html=~s/５/5/g;
	$html=~s/６/6/g;
	$html=~s/７/7/g;
	$html=~s/８/8/g;
	$html=~s/９/9/g;
	print $html;
} else {
	$_getcity=&encode($getcity);
	print<<FIN;
$html
[<a href="area.cgi?city=$_getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup&out=rss&m=$mode">RSS</a>]
FIN
	print &make_link_qrcode("$basehref?city=$_getcity&amp;gid=$getgroup&amp;m=$mode");
	printf("<hr>\nPowered by Perl $] HTML convert time to %.3f sec.",
		((times)[0] - $::_conv_start));
}
print <<FIN;
$debug
</body>
</html>
FIN

# ローマ字の1文字目を大文字、それ以降を小文字にする。
sub roma {
	my($buf)=@_;
	my $out;
	my $tmp;
	if($buf=~/^(.)(.+)$/) {
		$out=$1;
		$tmp=$2;
		$tmp=~tr/[A-Z]/[a-z]/;
		$out.=$tmp;
	}
	$out;
}

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
	$basehost = "$ENV{'HTTP_HOST'}";
	$basehost = 'http://' . $basehost;
	# Special Thanks to gyo
	$basehost .= ":$ENV{'SERVER_PORT'}"
		if ($ENV{'SERVER_PORT'} ne '80' && $basehost !~ /:\d/);
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
	$basehref=$basehost . $uri;
	$basepath=$uri;
	$basepath=~s/\/[^\/]*$//g;
	$basepath="/" if($basepath eq '');
	$script=$uri if($script eq '');
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

# カナ→ｶﾅ変換 from jcode.pl

sub z2h {
    local(*s, $n) = @_;
    $re_euc_c    = '[\241-\376][\241-\376]';
    $re_euc_kana = '\216[\241-\337]';
	from_to($s,'utf8','euc-jp');
    &init_z2h_euc;
    $s =~ s/($re_euc_c|$re_euc_kana)/
	$z2h_euc{$1} ? ($n++, $z2h_euc{$1}) : $1
    /geo;
	from_to($s,'euc-jp','utf8');
    $n;
}

sub init_z2h_euc {
    ($h2z_high = $h2z = <<'__TABLE_END__') =~ tr/\041-\176/\241-\376/;
!	!#	$	!"	%	!&	"	!V	#	!W
^	!+	_	!,	0	!<
'	%!	(	%#	)	%%	*	%'	+	%)
,	%c	-	%e	.	%g	/	%C
1	%"	2	%$	3	%&	4	%(	5	%*
6	%+	7	%-	8	%/	9	%1	:	%3
6^	%,	7^	%.	8^	%0	9^	%2	:^	%4
;	%5	<	%7	=	%9	>	%;	?	%=
;^	%6	<^	%8	=^	%:	>^	%<	?^	%>
@	%?	A	%A	B	%D	C	%F	D	%H
@^	%@	A^	%B	B^	%E	C^	%G	D^	%I
E	%J	F	%K	G	%L	H	%M	I	%N
J	%O	K	%R	L	%U	M	%X	N	%[
J^	%P	K^	%S	L^	%V	M^	%Y	N^	%\
J_	%Q	K_	%T	L_	%W	M_	%Z	N_	%]
O	%^	P	%_	Q	%`	R	%a	S	%b
T	%d			U	%f			V	%h
W	%i	X	%j	Y	%k	Z	%l	[	%m
\	%o	]	%s	&	%r	3^	%t
__TABLE_END__
    %h2z = split(/\s+/, $h2z . $h2z_high);
    %z2h = reverse %h2z;

    local($k, $s);
    while (($k, $s) = each %z2h) {
	$s =~ s/([\241-\337])/\216$1/g && ($z2h_euc{$k} = $s);
    }
}

sub read_timetable() {
	my %timetable;

	open my $fh, '<', 'timetable.txt' or die $!;
	while (<$fh>) {
		chomp;
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

sub load_module{
	my $mod = shift;
	eval qq( require $mod; );
	unless($@) {
		return 1;
	} else {
		return 0;
	}
}

sub make_link_qrcode {
	my ($string) = shift;
	if(&load_module("GD::Barcode")) {
		if($englishflg) {
			$buf="If you have movile phone to transfer this result, use this barcode.";
		} else {
			$buf="この検索結果を携帯に転送するには、このQRコードを読み込んで下さい。";
		}
		$string=&encode($string);
		return <<EOM;
<br />$buf<br />
<img alt="QRCode" src="$basehref?m=qr\&amp;str=$string" />
EOM
	}
	'';
}

sub make_qrcode {
	my ($string) = shift;
	my %hParm;
	my $oGdBar;

	$defaultECC='M';
	$defaultVersion=0;
	$defaultSize=3;

	if(&load_module("GD::Barcode")) {
		$hParm{Ecc}=$defaultECC;
		$hParm{ModuleSize}=$defaultSize;
		$hParm{Version}=1+int(
			length($string) / (
				($defaultECC eq 'H' ? 8 : $defaultECC eq 'Q' ? 12
		 		: $defaultECC eq 'M' ? 15 : 18)
				-2));
		$hParm{Version}=10;
		$oGdBar = GD::Barcode->new(
			'QRcode',
			$string,
			\%hParm);
		die($GD::Barcode::errStr) unless($oGdBar);

		binmode(STDOUT);
		print <<FIN;
Content-type: image/png

FIN
		print $oGdBar->plot->png;
		exit;
	}
}

