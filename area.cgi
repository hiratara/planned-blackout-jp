#!/usr/bin/perl

# nanakochi123456 version nyatakasan/hiratara 1st release:mnakajim

BEGIN {
	my $conv_start = (times)[0];
	require "fatlib.pl";
}
use utf8;
use strict;
use CGI;
use Encode qw/decode decode_utf8/;
use Encode::Guess;
use PlannedBlackoutJP::Util qw/is_galapagos/;
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
my $getgroup=$query->param('gid');
my $getgroup_sub=$query->param('gids');
if($getgroup>8 || $getgroup<=0) {
	$getgroup=0;
}
if($getgroup_sub!~/[0ABCDE]/) {
	$getgroup_sub=0;
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

# 電力会社リスト
my @company_list=(
	# 東京電力
	"茨城県,T","栃木県,T","群馬県,T","埼玉県,T","千葉県,T",
	"東京都,T","神奈川県,T","山梨県,T","静岡県,T",

	# 東北電力
	"青森県,H","秋田県,H","岩手県,H","宮城県,H","山形県,H",
	"福島県,H","新潟県,H"
);

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
	my %citys=&getzip($zip);
	$getcity="$citys{pref_ja}$citys{city_ja}$citys{town_ja}";
	$getcity=&addnor($getcity);
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

# 携帯かどうか？
my $mobileflg;
$mobileflg=1 if(is_galapagos(\%ENV) || $mflg);

# タイムテーブル取得

my $timetable = &read_timetable;
my @dates = map {$date[$_]} 0 .. 3;

# 実行状況取得
my $runtable = &read_runtable;

# 日付文字列を生成する。

if($englishflg) {
	for(my $i=0; $i<4; $i++) {
		$date_str[$i]="$mon[$i]/$mday[$i]";
	}
} else {
	for(my $i=0; $i<4; $i++) {
		$date_str[$i]="$mon[$i]月$mday[$i]日";
	}
}

my $areas;

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

# グループ検索
} elsif($getcity eq '') {
	my $firms="T,H";
	my %company_string;
	my %groups;
	if($englishflg) {
		$company_string{T}="Tepco Area";
		$company_string{H}="Tohoku Area";
	} else {
		$company_string{T}="東京電力";
		$company_string{H}="東北電力";
	}
	$groups{T}="1-A,1-B,1-C,1-D,1-E,2-A,2-B,2-C,2-D,2-E,3-A,3-B,3-C,3-D,3-E,4-A,4-B,4-C,4-D,4-E,5-A,5-B,5-C,5-D,5-E";
	$groups{H}="1,2,3,4,5,6,7,8";

	# 現状東京電力と東北電力のみだが、
	# 他の電力会社が計画停電をしたときの為にループ
	my @groups;
	foreach my $firm(split(/,/,$firms)) {
		my @nums;
		my @subs;
		foreach my $grp((split(/,/,$groups{$firm}))) {
			my($num,$group)=split(/\-/,$grp);
			if(($getgroup eq 0 && $getgroup_sub eq 0) ||
					($getgroup ne 0 && $getgroup eq $num && $getgroup_sub eq 0) ||
					($getgroup_sub ne 0 && $getgroup_sub eq $group && $getgroup eq 0) ||
					($getgroup ne 0 && $getgroup eq $num &&
					 $getgroup_sub ne 0 && $getgroup_sub eq $group)) {
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

				push @results, {
					tdfk => $company_string{$firm},
					shiku => '',
					machiaza => '',
					hour_refs => \@hour_refs,
					grp => $grp
				};
			}
		}
	}
	if($getgroup) {
		if($englishflg) {
			$areas="Group $getgroup@{[$getgroup_sub ? '-' . $getgroup_sub : '']}";
		} else {
			$areas="グループ $getgroup@{[$getgroup_sub ? '-' . $getgroup_sub : '']}";
		}
	} elsif($getgroup_sub) {
		if($englishflg) {
			$areas="SubGroup $getgroup_sub";
		} else {
			$areas="サブグループ $getgroup_sub";
		}
	} else {
		if($englishflg) {
			$areas="All Areas";
		} else {
			$areas="全エリア";
		}
	}
# 文字列検索
} else {
	open my $in, '<:utf8', "all.all" || &err("all.all can't read");
	my $firm;
	while (<$in>) {
		chomp;
		my ($area1,$area2,$area3,$num,$subgrp,$areaen1,$areaen2,$areaen3,$areakana1,$areakana2,$areakana3)=split (/\t/,$_);
		my $areaorg="$area1$area2$area3$areaen1$areaen2$areaen3$areakana1$areakana2$areakana3";
		$areaorg=&addnor($areaorg);

		next if $getgroup && $num != $getgroup;
		next if $subgrp ne '' && $getgroup_sub ne '0' && $subgrp ne $getgroup_sub;
		next unless $areaorg =~ m/$getcity/;
		my $areakanji;
		my $areakana;
		my $arearoma="$areaen1$areaen2$areaen3";
		my $grp=$subgrp ne '' ? "$num-$subgrp" : $num;

		foreach(@company_list) {
			my($_pref,$_firm)=split(/,/,$_);
			if($area1 eq $_pref) {
				$firm=$_firm;
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
}

if($out eq 'rss') {
	&gzip_compress("Content-type: text/xml;charset=utf-8\nCache-Control: max-age=0\nExpires: Mon, 26, Jul 1997 05:00:00 GMT");
} else {
	&gzip_compress("Content-type: text/html; charset=utf-8\nCache-Control: max-age=0\nExpires: Mon, 26, Jul 1997 05:00:00 GMT");
}

my $_getcity=&enc($titlename);
my $mtf = Text::MicroTemplate::File->new;
my $rss_link;
if($getcity!~/^(バージョン|試験|更新|[Uu][Pp][Dd][Aa][Tt][Ee]|[Vv][Ee][Rr])/) {
	$rss_link="area.cgi?city=$_getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup&gids=$getgroup_sub&out=rss&m=$mode";
}
my $html;
my $template=&gettemplate($out,$mobileflg, $englishflg);
if($out eq 'rss') {
	$html = $mtf->render_file(
		$template,
		$areas, \@date_str, \@results, $error_message, "$basehost$basepath",
		"$basehref?city=$_getcity&zip1=$zip1&zip2=$zip2&gid=$getgroup&gids=$getgroup_sub&m=$mode",
		&date("Y-m-dTH:i:s+9:00")
	);
} else {
	$html = $mtf->render_file(
		$template,
		$areas, \@date_str, \@results,
		$error_message, \@version_message, $rss_link,
		&make_link_qrcode("$basehref?city=$_getcity&amp;gid=$getgroup&amp;gids=$getgroup_sub&amp;m=$mode"),
		sprintf("Powered by Perl $] HTML convert time to %.3f sec.",
			((times)[0] - $::conv_start))
	);

	if($mobileflg) {
		$html=&z2h($html);
	}
}
print <<EOM;
<?xml version="1.0" encoding="UTF-8" ?>
$html$debug
EOM

# テンプレートファイル名指定
sub gettemplate {
	my ($out, $mobileflg, $englishflg)=@_;
	if($englishflg) {
		if($out eq 'rss') {
			$template="area_en_rss.xml";
		} elsif($mobileflg) {
			$template="area_en_m.html";
		} else {
			$template="area_en.html";
		}
	} else {
		if($out eq 'rss') {
			$template="area_jp_rss.xml";
		} elsif($mobileflg) {
			$template="area_jp_m.html";
		} else {
			$template="area_jp.html";
		}
	}
}

# 郵便番号→住所
sub getzip {
	my %citys;
	my($zip)=shift;
	my $zip1;
	my $zip2;
	if($zip=~/(\d\d\d)(\d\d\d\d)/) {
		$zip1=$1;
		$zip2=$2;
		$zip=$zip1 . $zip2;
	} else {
		return %citys;
	}

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
					my ($area1,$area2,$area3,$num,$subgrp,$areaen1,$areaen2,$areaen3,$areakana1,$areakana2,$areakana3)=split (/\t/,$_);
					if($kanji1 eq $area1 && $kanji2 eq $area2 && ($area3 =~/$kanji3/ || $kanji3 =~/$area3/)) {
						$citys{pref_ja}="$area1";
						$citys{city_ja}="$area2";
						$citys{town_ja}="$area3";
						$citys{pref_en}=&roma("$areaen1");
						$citys{city_en}=&roma("$areaen2");
						$citys{town_en}=&roma("$areaen3");
						last;
					}
				}
				close($in);
			}
		}
	}
	return %citys;
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
	return &find_version_line("all.all","version");
}

sub getzipdatabaseversion {
	return &find_version_line("yubin.csv","version");
}

sub gettimetableversion {
	return &find_version_line("timetable.txt","V");
}

sub find_version_line($$) {
	my ($file, $key) = @_;
	open my $in, '<:utf8', "$file" or &err($file);

	while (<$in>) {
		chomp;
		my ($cur_key, $left) = split /\t/, $_, 2;
		if ($cur_key eq $key) {
			return $left;
		}
	}
	return '--';
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
	my $orgstr=shift;
	$orgstr =~ tr/がケヶのノ　 /ケケケのの/d;

	# remove '字' and '大字'
	$orgstr =~ s/([市区町村])大?字/$1/;
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
