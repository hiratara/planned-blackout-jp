#!/usr/bin/perl

# nanakochi123456 version nyatakasan/hiratara 1st release:mnakajim

BEGIN {
	my $conv_start = (times)[0];
}
use strict;
use CGI;
use Encode qw/decode encode_utf8 from_to/;
use Encode::Guess;

my $debug;
require "common.pl";
require "counter.pl";

# query 取得等

my $query=new CGI;

# QRコードモードならイメージ生成のみをする。

my $getcity=$query->param('city');
$getcity=&force_utf8($query->param('city'));
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
$getcity=~ s/ //g;
$getcity=~ s/　//g;
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
	open (R,"yubin.csv");
	while(<R>) {
		chomp;
		push(@ZIP,$_);
	}
	close(R);
	if($zip2 ne "0000") {
		foreach(@ZIP) {
			s/ケ/ヶ/g;
			s/の/ノ/g;
			my ($ziptmp,$kanji1,$kanji2,$kanji3)=split(/\t/,$_);
			if($ziptmp eq $zip) {
				open (READ,"all.all");
				while (<READ>) {
					chomp;
					my ($area1,$area2,$area3,$num)=split (/\t/,$_);
					if($kanji1 eq $area1 && $kanji2 eq $area2 && ($area3 =~/$kanji3/ || $kanji3 =~/$area3/)) {
						$getcity="$area1$area2$area3";
						$getcity=&addnor($getcity);
						last;
					}
				}
				close(READ);
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
	my $_getcity=&encode($getcity);
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
		open (READ,"all.all");
		while (<READ>) {
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

			for(my $i=0; $i<$mobileflg; $i++) {
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
				$hours ? join(', ', @$hours) : '-';
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
<description>@{[$arearoma=~m/$getcity/ ? ($_=~/なし/ ? 'No execution' : $_) : "$_です。"]}</description>
<dc:date>$rssdate</dc:date>
</item>
FIN
				}
				++$i;
			}
			++$count;
		}
		for(my $i=0; $i<$mobileflg; $i++) {
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
<title>$areasの計画停電予定</title>
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

my $buf;
my $count=0;
my $head;
# 携帯出力
if($mobileflg eq 2) {
	$buf='';
	# エラー出力
	if($getcity=~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
		$buf="Engine Version:@{[&getengineversion]}<br />DataBase Version:@{[&getdatabaseversion]}<br />TimeTable Version:@{[&gettimetableversion]}<br />RunTable Version:<br />@{[&getruntableversion]}<br />ZIP Database Version: @{[&getzipdatabaseversion]}<br /><br />";
	} elsif ($zip2 eq "0000") {
		if($englishflg) {
			$buf="Ending in 0000 can not find the ZIP code.<br /><br />";
		} else {
			$buf="郵便番号末尾４桁 0000 では検索できません。<br /><br />";
		}
	} elsif ($zip ne '' && $zip!~/\d\d\d\d\d\d\d/ && length($zip) ne 7) {
		if($englishflg) {
			$buf="The ZIP code seems not to be input accurately.<br /><br />";
		} else {
			$buf="郵便番号が正確に入力されていないようです。<br /><br />";
		}
	} elsif($zip eq '' && $getcity eq '') {
		if($englishflg) {
			$buf="It's not input city name or ZIP code.<br /><br />";
		} else {
			$buf="地域名、もしくは郵便番号が入力されていません。<br /><br />";
		}
	} else {
		open (READ,"all.all");
		my $firm;
		my @outdate;
		my @time;
		while (<READ>) {
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
				$hours[$i] .=' ('.$tmp.')' if($tmp ne '');
			}

			for(my $i=0; $i<4; $i++) {
				if($englishflg) {
					$outdate[$i]=<<FIN;
[Schedule on $mon[$i]/$mday[$i]]<br />
FIN
				} else {
					$outdate[$i]=<<FIN;
【$mon[$i]月$mday[$i]日の予定】<br />
FIN
				}
			}
			my $i=0;
			foreach(@hours) {
				my $hours = $timetable->{$firm}{$_}{$num};
				my $hours ? join(', ', @$hours) : '-';
				my $outarea;
				if ($englishflg) {
					$outarea="@{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]}";
					$time[$i].=<<FIN;
$outarea<br />
[$grp]@{[$arearoma=~m/$getcity/ ? ($_=~/なし/ ? 'No execution' : $_) : "$_"]}<br />
FIN
				} else {
					$areakanji=&addnor("$area1$area2$area3");
					$areakana=&addnor("$areakana1$areakana2$areakana3");
					if($areakana=~ m/$getcity/) {
						$outarea="$areakana1 $areakana2 $areakana3";
					} elsif($arearoma=~ m/$getcity/) {
						$outarea="@{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]}";
					} else {
						$outarea="$area1$area2$area3";
					}
					$time[$i].=<<FIN;
$outarea<br />
[$grp]@{[$arearoma=~m/$getcity/ ? ($_=~/なし/ ? 'No execution' : $_) : "$_"]}<br />
FIN
				}
				++$i;
			}
			++$count;
		}
		for(my $i=0; $i<4; $i++) {
			$buf.="$outdate[$i]$time[$i]<br />";;
		}
		if (!$count) {
			if($englishflg) {
				$buf="Not found of rolling blakout area.<br /><br />";
			} else {
				$buf="計画停電のないエリアです。<br /><br />";
			}
		}
		if ($count>400) {
			if($englishflg) {
				$buf="There are a lot of pertinent regions. Please input a regional name of details.<br /><br />";
			} else {
				$buf="該当地域が多すぎです。詳細の地域名を入力してください。<br /><br />";
			}
		}
	}
	$buf="<br />$buf";
} else {
# HTML出力
	# 最初のtableタグの１行目を生成する。
	if($englishflg) {
		$buf=<<FIN;
	<table border=1><tr bgcolor=#C0C0C0><th>Areas</th>
FIN
		for(my $i=0; $i<$mobileflg; $i++) {
			$buf.=<<FIN;
	<th>$mon[$i]/$mday[$i] Blackout time.</th>
FIN
		}
		$buf.=<<FIN;
	<th>Group No</th></tr></tr>
FIN
	} else {
		$buf=<<FIN;
	<table border=1><tr bgcolor=#C0C0C0><th>地域</th>
FIN
		for(my $i=0; $i<$mobileflg; $i++) {
			$buf.=<<FIN;
	<th>$mon[$i]月$mday[$i]日停電時間</th>
FIN
		}
		$buf.=<<FIN;
	<th>グループ</th></tr></tr>
FIN
	}

	$head=$buf;
	$buf='';
	# エラー出力
	if($getcity=~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
		$buf="<tr><td colspan=1>Engine Version:</td><td colspan=5>@{[&getengineversion]}</td></tr><tr><td colspan=1>DataBase Version: </td><td colspan=5>@{[&getdatabaseversion]}</td></tr><tr><td colspan=1>TimeTable Version:</td><td colspan=5>@{[&gettimetableversion]}</td></tr><tr><td colspan=1>RunTable Version:</td><td colspan=5>@{[&getruntableversion]}</td></tr><tr><td colspan=1>ZIP Database Version: </td><td colspan=5>@{[&getzipdatabaseversion]}</td></tr>";
	} elsif ($zip2 eq "0000") {
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
		my $firm;
		my $bgcolor;
		while (<READ>) {
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

			if ($count % 2 ==0) {
				$bgcolor=' bgcolor=EEFFFF';
			} else {
				$bgcolor=' bgcolor=FFEEFF';
			}
			my @hours = map {
				my $hours = $timetable->{$firm}{$_}{$num};
				$hours ? join(', ', @$hours) : '-';
			} @dates;

			for(my $i=0; $i<$mobileflg; $i++) {
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
				$hours[$i] .='<br />('.$tmp.')' if($tmp ne '');
			}

			if($englishflg) {
				$buf.="<tr$bgcolor><td><b>@{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]}</b></td>" . 
				      join('', map {"<td>$_</td>"} @hours) . 
				      "<td>Group $grp</td></tr>\n";

			} else {
				$areakanji=&addnor("$area1$area2$area3");
				$areakana=&addnor("$areakana1$areakana2$areakana3");
				$arearoma=&addnor("$areaen1$areaen2$areaen3");
				if($areakanji=~ m/$getcity/) {
					$buf.="<tr$bgcolor><td><b>$area1 $area2 $area3</b></td>"
						. join('', map {"<td>$_</td>"} @hours) . 
						      "<td>第$grpグループ</td></tr>\n";

				} elsif($areakana=~ m/$getcity/) {
					$buf.="<tr$bgcolor><td><b>$areakana1 $areakana2 $areakana3</b></td>"
						. join('', map {"<td>$_</td>"} @hours) . 
						      "<td>ダイ$grpグループ</td></tr>\n";
				} elsif($arearoma=~ m/$getcity/) {
					$buf.="<tr$bgcolor><td><b>@{[&roma($areaen1)]} @{[&roma($areaen2)]} @{[&roma($areaen3)]}</b></td>"
						. join('', map {"<td>@{[$_ =~/なし/ ? 'No execution' : $_]}</td>"} @hours) . 
						      "<td>Group $grp</td></tr>\n";
				}
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

my $html;
if($englishflg) {
	$html=<<FIN;
<html><head>
<title>$areas of Rolling blackout schedule</title></head><body>
@{[$mobileflg eq 4 ? '<table><tr><td><img src="kekka_eng.jpg" width="200"></td><td>' : '']}
Found $count. The schedule time is different when there are two or more registration in the same region according to the place.<BR>
When the power failure twice a day is scheduled, the power failure schedule in the latter half is executed according to the situation. <BR>
You can bookmark rhis page for next use. <BR>
@{[$mobileflg eq 4 ? '</td></tr></table>' : '']}
$head
$buf
</table>
[<a href=./?e>Return</a>] 
FIN
} else {
	$html=<<FIN;
<html><head>
<title>$areasの計画停電予定</title></head><body>
@{[$mobileflg eq 4 ? '<table><tr><td><img src="kekka.jpg" width="200"></td><td>' : '']}
$count件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。<BR>
1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<BR>
このページをブックマークしておくと、ブックマーク呼び出しだけで地域名または郵便番号の入力が不要です。 <BR>
@{[$mobileflg eq 4 ? '</td></tr></table>' : '']}
$head
$buf
</table>
[<a href=./>戻る</a>] 
FIN
}

# 携帯なら、全角数字を及び全角カナを半角に変換する。
if($mobileflg eq 2 || $mflg eq 1) {
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
	print $html;
} else {
# PC用出力
	my $_getcity=&encode($titlename);
	print<<FIN;
$html
FIN

# RSS出力＆QRコード生成
	if($getcity!~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
		print <<FIN;
[<a href="area.cgi?city=$_getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup_tepco&gids=$getgroup_tepco_sub&gidh=$getgroup_tohoku&out=rss&m=$mode">RSS</a>]
FIN
		print &make_link_qrcode("$basehref?city=$_getcity&amp;gid=$getgroup_tepco&amp;gids=$getgroup_tepco_sub&amp;gidh=$getgroup_tohoku&amp;m=$mode");
	}
# 変換時間表示
	printf("<hr>\nPowered by Perl $] HTML convert time to %.3f sec.",
		((times)[0] - $::_conv_start));
}
print <<FIN;
$debug
</body>
</html>
FIN

# 結果表示の画像表示
sub result_img {
	my($file)=shift;
	my $body;
	if($mobileflg eq 4) {
		$body=<<EOM;
<img src="$file" width="200"><br />
EOM
	}
	$body;
}

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

# by hiratara 携帯のGETでShiftJISが送信される可能性をUTF8に強制変換する。

sub force_utf8($) {
	my $str = shift || '';
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? encode_utf8($enc->decode($str)) : $str;
}

# タイムテーブル読み込み

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

# 実行テーブル読み込み

sub read_runtable() {
	my %runtable;
	open my $fh, '<', 'runtable.txt' or die $!;
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
		if($englishflg) {
			$buf="<br />If you have mobile phone to transfer this result, use this barcode.";
		} else {
			$buf="<br />この検索結果を携帯に転送するには、このQRコードを読み込んで下さい。";
		}
		$string=&encode($string);
		return <<EOM;
<br />$buf<br />
<img alt="QRCode" src="$basehref?m=qr\&amp;str=$string\&amp;qr=result" />
EOM
	}
	'';
}

sub getengineversion {
	my $VER;
	open(R,"index.cgi");
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
	open (READ,"all.all");
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
	open (READ,"yubin.csv");
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
	open (READ,"timetable.txt");
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
	open (READ,"runtable.txt");
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
