#!/usr/bin/perl

# nanakochi123456 version nyatakasan/hiratara 1st release:mnakajim

BEGIN {
	my $conv_start = (times)[0];
	require "fatlib.pl";
}
use utf8;
use strict;
use CGI;
use Encode qw/decode encode_utf8 from_to decode_utf8/;
use Encode::Guess;
use Text::MicroTemplate::File;

my $debug;
my $error_message;
my @version_message;
require "common.pl";
require "counter.pl";

# query 取得等

my $query=new CGI;

# QRコードモードならイメージ生成のみをする。

my $getcity=$query->param('city');
$getcity=force_decode($query->param('city'));
my $zip=$query->param('zip');
my $zip1;
my $zip2;
my $mode=$query->param('m');
my $qr=$query->param('qr');
my $englishflg=0;
$englishflg=1 if($mode=~/e/);
my $mflg=0;
$mflg=1 if($mode=~/m/);
my $kanaflg=0;
my @results;
my @date_str;

if($mode eq 'qr') {
	my $string=$query->param('str');
	&make_qrcode($string,$qr);
	exit;
}

$getcity=~ s/　//g;
$getcity=~ s/ //g;

$zip=~s/\-//g;

# 携帯向け
if($zip eq '') {
	$zip1=$query->param('zip1');
	$zip2=$query->param('zip2');
	$zip=$zip1 . $zip2;
}

if($zip=~/(\d\d\d)(\d\d\d\d)/) {
	$zip1=$1;
	$zip2=$2;
	$zip=$zip1 . $zip2;
}

my $out=$query->param('out');
my $comm=$query->param('comm');
my $getgroup_tepco=$query->param('gid');
my $getgroup_tepco_sub=$query->param('gids');
my $getgroup_tohoku=$query->param('gidh');
my $getgroup;
if($getgroup_tepco=~/^(\d)\-(.)$/) {
	if($1>5 || $1<=0) {
		$getgroup=0;
	} else {
		$getgroup="$1-$2";
	}
} elsif($getgroup_tepco=~/^(\d)$/ && $getgroup_tepco_sub=~/^[ABCDE]$/) {
	if($getgroup_tepco>5 || $getgroup_tepco<=0) {
		$getgroup=0;
	} else {
		$getgroup="$getgroup_tepco\-$getgroup_tepco_sub";
	}
} elsif($getgroup_tohoku=~/^(\d)$/) {
	if($getgroup_tohoku>8 || $getgroup_tohoku<=0) {
		$getgroup=0;
	} else {
		$getgroup=$getgroup_tohoku;
	}
}

# 地域名入力欄から郵便番号を取得する。
my $ziptmp=$getcity;
$ziptmp=~s/０/0/g;
$ziptmp=~s/１/1/g;
$ziptmp=~s/２/2/g;
$ziptmp=~s/３/3/g;
$ziptmp=~s/４/4/g;
$ziptmp=~s/５/5/g;
$ziptmp=~s/６/6/g;
$ziptmp=~s/７/7/g;
$ziptmp=~s/８/8/g;
$ziptmp=~s/９/9/g;
$ziptmp=~s/－//g;
$ziptmp=~s/ー//g;
$ziptmp=~s/-//g;

if($ziptmp=~/(\d\d\d)(\d\d\d\d)/) {
	$zip1=$1;
	$zip2=$2;
	$zip=$zip1 . $zip2;
}

# 東京電力リスト
my @tokyo_denryoku_list=("茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","山梨県","静岡県");

# 東北電力リスト
my @tohoku_denryoku_list=("青森県","秋田県","岩手県","宮城県","山形県","福島県","新潟県");

# 各種変換
my $titlename=$getcity;
$getcity=&addnor($getcity);
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

# 一時大文字変換をする。
$getcity=~tr/[a-z]/[A-Z/;

# バージョン情報表示
if($comm eq 'ver') {
	my $ver=&getengineversion;
	my $timetable=&gettimetableversion();
	my $areatable=&getdatabaseversion();
	my $runtable=&getruntableversion();
	my $counter=&counter_get();
	print <<FIN;
Content-type: text/plain; charset=utf-8

area.cgi : $ver
timetable.txt : $timetable
areatable.txt : $areatable
runtable.txt  : $runtable
$counter
FIN
	exit;
}

&counter_write();

# $getbasehref に スクリプトの実パスが入る。
my($basehref, $basehost, $basepath)=&getbasehref;

# 郵便番号検索
if($zip ne '') {
	my @ZIP=();
	open my $in, '<:utf8', "yubin.csv" || &err("yubin.csv can't read");
	while(<$in>) {
		chomp;
		push(@ZIP,$_);
	}
	close($in);
	if($zip2 ne "0000") {
		foreach(@ZIP) {
			s/ケ/ヶ/g;
			s/の/ノ/g;
			my ($ziptmp,$kanji1,$kanji2,$kanji3)=split(/\t/,$_);
			if($ziptmp eq $zip) {
				open my $in, '<:utf8', "all.all" || &err("all.all can't read");
				while (<$in>) {
					chomp;
					my ($area1,$area2,$area3,$num)=split (/\t/,$_);
					if($kanji1 eq $area1 && $kanji2 eq $area2 && ($area3 =~/$kanji3/ || $kanji3 =~/$area3/)) {
						$getcity="$area1$area2$area3";
						$getcity=&addnor($getcity);
						last;
					}
				}
				close($in);
			}
		}
	}
}

# 日付取得
my @date;
my @mon;
my @mday;

for(my $i=0; $i<5; $i++) { 
	$date[$i]=&date("Y-m-d",,time+86400*$i);
	$mon[$i]=&date("n",,time+86400*$i);
	$mday[$i] = &date("j",,time+86400*$i);
}

# 携帯かどうか？ ループ数カウントも含めるため、それぞれの数字になってます。

my $mobileflg;
$mobileflg=4;
$mobileflg=2 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE/) || $mflg eq 1;

# タイムテーブル取得

my $timetable = &read_timetable;
my @dates = map {$date[$_]} 0 .. 3;

# 実行状況取得
my $runtable = &read_runtable;

# rss出力
if($out eq 'rss') {
	my $buf='';
	my $rssdate=&date("Y-m-dTH:i:s+9:00");

	my $count=0;
	my $_getcity=&enc($getcity);
	my $xml;

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
		my $firm;
		my @xmldate;
		open my $in, '<:utf8', "all.all" || &err("all.all can't read");
		while (<$in>) {
			chomp;
			my ($area1,$area2,$area3,$num,$subgrp,$areaen1,$areaen2,$areaen3,$areakana1,$areakana2,$areakana3)=split (/\t/,$_);
			my $areaorg="$area1$area2$area3$areaen1$areaen2$areaen3$areakana1$areakana2$areakana3";
			$areaorg=&addnor($areaorg);
			my $areakanji;
			my $areakana;
			my $arearoma="$areaen1$areaen2$areaen3";
			my $grp=$subgrp ne '' ? "$num-$subgrp" : $num;

			if ($getgroup) {
				next unless $areaorg=~ m/$getcity/ and $grp eq $getgroup;
			} else {
				next unless $areaorg=~ m/$getcity/;
			}

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

			my @hours = map {
				my $hours = $timetable->{$firm}{$_}{$num};
				$hours ? join(', ', @$hours) : '-';
			} @dates;

			for(my $i=0; $i<4; $i++) {
				my $tmp=$runtable->{$firm}{$date[$i]}{$grp};
				if($englishflg) {
					if($tmp=~/午前/) {
						$tmp="AM only";
					} elsif($tmp=~/午後/) {
						$tmp="PM only";
					} elsif($tmp=~/せず/ || $tmp=~/中止/) {
						$tmp="No execution";
					} elsif($tmp=~/予定/) {
						$tmp="Scheduled";
					} elsif($tmp eq '') {
						$tmp="";
					} else {
						$tmp="Execution";
					}
					if($hours[$i]=~/なし/) {
						$hours[$i]="No execution";
					}
				}
				$hours[$i] .='('.$tmp.')' if($tmp ne '');
			}

			my $i=0;
			foreach(@hours) {
				my $hours = $timetable->{$firm}{$_}{$num};
				my $hour ? join(', ', @$hours) : '-';
				if ($englishflg) {
					if(/なし/) {
						$_="No execution";
					}
					$xmldate[$i].=<<FIN;
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku">
<title>[$mon[$i]/$mday[$i]] @{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]} (group $grp) of rolliing blackout infomation.</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku</link>
<description>$_</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
				} else {
					my $outarea;
					my $xmltitle;
					$areakanji=&addnor("$area1$area2$area3");
					$areakana=&addnor("$areakana1$areakana2$areakana3");
					if($areakana=~ m/$getcity/) {
						$outarea="$areakana1 $areakana2 $areakana3";
						$xmltitle="【$mon[$i]月$mday[$i]日】$outarea(グループ$grp)の計画停電情報です。";
					} elsif($arearoma=~ m/$getcity/) {
						$outarea="$areaen1 $areaen2 $areaen3";
						$xmltitle="[$mon[$i]/$mday[$i]日] $outarea (group $grp) of rolliing blackout infomation.";
					} else {
						$outarea="$area1$area2$area3";
						$xmltitle="【$mon[$i]月$mday[$i]日】$outarea(グループ$grp)の計画停電情報です。";
					}
					$xmldate[$i].=<<FIN;
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku">
<title>$xmltitle</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku</link>
<description>@{[$arearoma=~m/$getcity/ ? ($_=~/なし/ ? 'No execution' : $_) : "$_ です。"]}</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
				}
				++$i;
			}
			++$count;
		}
		for(my $i=0; $i<4; $i++) {
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
		close($in);
	}

	my $areas;
	if($zip ne '') {
		if($englishflg) {
			$areas="ZIP:$zip1-$zip2";
		} else {
			$areas="〒$zip1-$zip2";
		}
	} else {
		$areas=$titlename;
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
<channel rdf:about="$basehost$basepath">
<title>$areas of rolling blackout schedule</title>
<link>$basehref</link>
</channel>
<item rdf:about="$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku">
<title>$buf</title>
<link>$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku</link>
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
<channel rdf:about="$basehost$basepath">
<title>$areas の計画停電予定</title>
<link>$basehost/index.html</link>
</channel>
<item rdf:about="$basehref?city=$_getcity&amp;zip1=$zip1&amp;zip2=$zip2&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku">
<title>$buf</title>
<link>$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku</link>
<dc:date>$rssdate</dc:date>
</item>
FIN
		} else {
			print <<FIN;
<channel rdf:about="$basehost$basepath">
<title>$areas の計画停電予定</title>
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

# HTML出力
# 最初のtableタグの１行目を生成する。
if($englishflg) {
	for(my $i=0; $i<4; $i++) {
		$date_str[$i]="$mon[$i]/$mday[$i]";
	}
} else {
	for(my $i=0; $i<4; $i++) {
		$date_str[$i]="$mon[$i]月$mday[$i]日";
	}
}
# エラー出力
if($getcity=~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
	@version_message=&getversion;
	$error_message="version";
} elsif ($zip2 eq "0000") {
	if($englishflg) {
		$error_message="Ending in 0000 can not find the ZIP code.";
	} else {
		$error_message="郵便番号末尾４桁 0000 では検索できません。";
	}
} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
	if($englishflg) {
		$error_message="The ZIP code seems not to be input accurately.";
	} else {
		$error_message="郵便番号が正確に入力されていないようです。";
	}
} elsif($zip eq '' && $getcity eq 'aa') {
	if($englishflg) {
		$error_message="It's not input city name or ZIP code.";
	} else {
		$error_message="地域名、もしくは郵便番号が入力されていません。";
	}
} else {
	open my $in, '<:utf8', "all.all" || &err("all.all can't read");
	my $firm;
	while (<$in>) {
		chomp;
		my ($area1,$area2,$area3,$num,$subgrp,$areaen1,$areaen2,$areaen3,$areakana1,$areakana2,$areakana3)=split (/\t/,$_);
		my $areaorg="$area1$area2$area3$areaen1$areaen2$areaen3$areakana1$areakana2$areakana3";
		$areaorg=&addnor($areaorg);
		my $areakanji;
		my $areakana;
		my $arearoma="$areaen1$areaen2$areaen3";
		my $grp=$subgrp ne '' ? "$num-$subgrp" : $num;

		next if $getgroup && $grp != $getgroup;
		next unless $areaorg =~ m/$getcity/;

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

		my @hour_refs = map {
			my $hours = $timetable->{$firm}{$_}{$num};
			my $run_str = $runtable->{$firm}{$_}{$grp} || '';
			my $hours_str = $hours ? join(', ', @$hours) : '-';
			if($englishflg) {
				if($run_str=~/午前/) {
					$run_str="AM only";
				} elsif($run_str=~/午後/) {
					$run_str="PM only";
				} elsif($run_str=~/せず/ || $run_str=~/中止/) {
					$run_str="No execution";
				} elsif($run_str=~/予定/) {
					$run_str="Scheduled";
				} elsif($run_str eq '') {
					$run_str="";
				} else {
					$run_str="Execution";
				}
				$hours_str=~s/実施なし/No execution/g;
			}
			{hours_str => $hours_str, run_str => $run_str};
		} @dates;

		if($englishflg) {
			push @results, {
				tdfk => &roma($areaen1), 
				shiku => &roma($areaen2), 
				machiaza => &roma($areaen3),
				hour_refs => \@hour_refs,
				grp => $grp
			};
		} else {
			$areakanji=&addnor("$area1$area2$area3");
			$areakana=&addnor("$areakana1$areakana2$areakana3");
			$arearoma=&addnor("$areaen1$areaen2$areaen3");
			if($areakanji=~ m/$getcity/) {
				push @results, {
					tdfk => $area1, 
					shiku => $area2, 
					machiaza => $area3,
					hour_refs => \@hour_refs,
					grp => $grp
				};
			} elsif($areakana=~ m/$getcity/) {
				push @results, {
					tdfk => $areakana1, 
					shiku => $areakana2, 
					machiaza => $areakana3,
					hour_refs => \@hour_refs,
					grp => $grp
				};
			} elsif($arearoma=~ m/$getcity/) {
				push @results, {
					tdfk => &roma($areaen1), 
					shiku => &roma($areaen2), 
					machiaza => &roma($areaen3),
					hour_refs => \@hour_refs,
					grp => $grp
				};
			}
		}
	}
	if (! @results) {
		if($englishflg) {
			$error_message="Not found of rolling blakout area.";
		} else {
			$error_message="計画停電のないエリアです。";
		}
		$error_message = "計画停電のないエリアです。";
	} elsif (@results > 400) {
		if($englishflg) {
			$error_message="There are a lot of pertinent regions. Please input a regional name of details.";
		} else {
			$error_message="該当地域が多すぎです。詳細の地域名を入力してください。";
		}
	}
	close($in);
}

my $areas;

if($zip ne '') {
	if($englishflg) {
		$areas="ZIP:$zip1-$zip2";
	} else {
		$areas="〒$zip1-$zip2";
	}
} else {
	$areas=$titlename;
}
$areas=~ s/[;\"\'\$\@\%\(\)]//g;	# by @mnakajim

&gzip_compress("Content-type: text/html; charset=utf-8\nCache-Control: max-age=0\nExpires: Mon, 26, Jul 1997 05:00:00 GMT");

my $_getcity=&enc($getcity);
my $mtf = Text::MicroTemplate::File->new;
my $rss_link;
if($getcity!~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
	$rss_link="area.cgi?city=$_getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup_tepco&gids=$getgroup_tepco_sub&gidh=$getgroup_tohoku&out=rss&m=$mode";
}
my $html;
my $template;
if($englishflg) {
	if($mobileflg eq 2) {
		$template="area_en_m.html";
	} else {
		$template="area_en.html";
	}
} else {
	if($mobileflg eq 2) {
		$template="area_jp_m.html";
	} else {
		$template="area_jp.html";
	}
}
my $html = $mtf->render_file(
	$template,
	$areas, \@date_str, \@results,
	$error_message, \@version_message, $rss_link,
	&make_link_qrcode("$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku&amp;m=$mode"),
	sprintf("Powered by Perl $] HTML convert time to %.3f sec.",
		((times)[0] - $::conv_start))
);
if($mobileflg eq 2) {
	$html=&z2h($html);
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
}
print <<EOM;
<?xml version="1.0" encoding="UTF-8" ?>
$html$debug
EOM

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

# 日付取得 - 面倒なのでpyukiwikiから移植ｗ

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

# $basehref 取得 - これも面倒だからpyukiwikiから移植
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
}

sub force_decode($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? $enc->decode($str) : decode_utf8($str);
}

# タイムテーブル読み込み

sub read_timetable() {
	my %timetable;

	open my $fh, '<:utf8', 'timetable.txt' || &err("timetable.txt can't read");
	while (<$fh>) {
		chomp;
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

# 実行テーブル読み込み

sub read_runtable() {
	my %runtable;
	open my $fh, '<:utf8', 'runtable.txt' || &err("runtable.txt can't read");
	while (<$fh>) {
		chomp;
		my ($firm,$date, $group, $state) = split /\t/, $_;
		$runtable{$firm}{$date}{$group} = $state;
	}
	close $fh;
	return \%runtable;
}

# QRコードの画像のリンクを作成
sub make_link_qrcode {
	my ($string) = shift;
	if(&load_module("GD") && &load_module("GD::Barcode")) {
		$string=&enc($string);
		return "$basehref?m=qr\&amp;str=$string\&amp;qr=result";
	}
	'';
}

sub getversion {
	return  (
		"Engine Version : " . &getengineversion,
		"DataBase Version : " . &getdatabaseversion,
		"TimeTable Version : " . &gettimetableversion,
		"RunTable Version : " . &getruntableversion,
		"ZIP Database Version : " . &getzipdatabaseversion
	);
}

sub getengineversion {
	my $VER;
	open(R,"index.cgi") || &err("index.cgi can't read");
	foreach(<R>) {
		if(/my\s\$VER\=\"V\.(.+)\"\;/) {
			$VER=$1;
			close(R);
			return $VER;
		}
	}
	close(R);
	return "What version ? or older";
}

sub getdatabaseversion {
	open (READ,"all.all") || &err("all.all can't read");
	while (<READ>) {
		chomp;
		my ($field,$ver)=split (/\t/,$_);
		if($field eq "version") {
			close(READ);
			return $ver;
		}
	}
	close(READ);
	return "What version ? or older";
}

sub getzipdatabaseversion {
	open (READ,"yubin.csv") || &err("yubin.csv can't read");
	while (<READ>) {
		chomp;
		my ($field,$ver)=split (/\t/,$_);
		if($field eq "version") {
			close(READ);
			return $ver;
		}
	}
	close(READ);
	return "What version ? or older";
}

sub gettimetableversion {
	open (READ,"timetable.txt") || &err("timetable.txt can't read");
	while(<READ>) {
		chomp;
		my ($firm,$ver)=split(/\t/,$_);
		if($firm eq "V") {
			close(READ);
			return $ver;
		}
	}
	close(READ);
	return "What version ? or older";
}

sub getruntableversion {
	open (READ,"runtable.txt") || &err("runtable.txt can't read");
	while(<READ>) {
		chomp;
		my ($firm,$ver)=split(/\t/,$_);
		if($firm eq "V") {
			close(READ);
			return $ver;
		}
	}
	close(READ);
	return "What version ? or older";
}

sub addnor() {
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

sub err {
	my $msg=shift;
	print <<EOM;
Content-type: text/html; charset=utf8

<html>
<head>
<title>area.cgi error</title>
</head>
<body>
<h1>Error</h1>
<hr>
$msg
</body>
</html>
EOM
	exit;
}
