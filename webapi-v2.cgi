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
@g19=('', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-12:20, 16:50-20:30', '12:20-15:20', '15:20-18:20');
@g20=('', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30', '12:20-16:00');

open (READ,"all.all");

$buf='';
$count=0;

while (<READ>) {
	chomp;
	($area1,$area2,$area3,$num)=split (/\t/,$_);
	$num = 0 if ! defined $num ;
	$areaorg="$area1$area2$area3";
	$areaorg=~ s/ //g;

	if ($getgroup) {
		if ($areaorg=~ m/$getcity/ and $num eq $getgroup) {
			$buf.="<Result><Area>$area1 $area2 $area3</Area><PowerOutTime>$g18[$num]</PowerOutTime><PowerOutTime>$g19[$num]</PowerOutTime><PowerOutTime>$g20[$num]</PowerOutTime><Group>${num}</Group></Result>";
			++$count;
		}
	} else {
		if ($areaorg=~ m/$getcity/) {
			$buf.="<Result><Area>$area1 $area2 $area3</Area><PowerOutTime>$g18[$num]</PowerOutTime><PowerOutTime>$g19[$num]</PowerOutTime><PowerOutTime>$g20[$num]</PowerOutTime><Group>${num}</Group></Result>";
			++$count;
		}
	}
}

if (!$count) {
	$buf="<Message>計画停電のないエリアとおもわれます。もしかすると地域名が狭すぎるかもしれません。もう少し広い地域名で検索することをおすすめします。</Message>";
}
if ($count>400) {
	$buf="<Result><Message>地域名が広過ぎます。もう少し狭い地域名を入力してください。</Message></Result>";
}

print "Content-type: text/xml\n\n";
print qq!<?xml version="1.0" encoding="utf-8" ?>\n<ResultSet DataVersion="V.1.112" ResultRows="$count" >$buf</ResultSet>!;

