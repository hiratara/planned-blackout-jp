#!/usr/bin/perl

use CGI ;
use constant {
    StartDAY => 1300374000, # 2011/3/18 0:0:0
    Sec_OF_Day => 86400 # 24 * 60 * 60
} ;

$query=new CGI;
$getcity=$query->param('city');
$getcity=~ s/ //g;
$getcity=~ s/　//g;
$getcity=~ s/0/０/g; #tr didnt work
$getcity=~ s/1/１/g;
$getcity=~ s/2/２/g;
$getcity=~ s/3/３/g;
$getcity=~ s/4/４/g;
$getcity=~ s/5/５/g;
$getcity=~ s/6/６/g;
$getcity=~ s/7/７/g;
$getcity=~ s/8/８/g;
$getcity=~ s/9/９/g;

$getgroup=$query->param('gid');
if ($getgroup>5 || $getgroup<=0) {
	$getgroup=0;
}

###############################################################
## this is undocumented rule seen from tepco released schedule.
###############################################################

@g0=('', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00');

@g1=('', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-12:20, 16:50-20:30', '12:20-15:20', '15:20-18:20');

@g2=('', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30', '12:20-16:00');

@g3=('', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30', '09:20-13:00, 16:50-20:30');

@g4=('', '09:20-13:00, 16:50-20:30', '12:20-16:00', '15:20-19:00', '18:20-22:00', '06:20-10:00, 13:50-17:30');

my $diff_ep =  int((time - StartDAY) / Sec_OF_Day % 5) ;

my $idx_1 = $diff_ep;
my $idx_2 = ++$diff_ep > 4 ? 1 : $diff_ep ;
my $idx_3 = ++$diff_ep > 4 ? 1 : $diff_ep ;

my @Groups = ( \@g0, \@g1, \@g2, \@g3, \@g4 );

open (READ,"all.all");

$buf='';
$count=0;

while (<READ>) {
	chomp;
	($area1,$area2,$area3,$num)=split (/\t/,$_);
	$num = 0 if ! defined $num ; #by sigemasa
	$area3_m = $area3; #by sigemasa
	$area3_m =~ s/^大字//; #by sigemasa
	$areaorg="$area1$area2$area3_m"; #by sigemasa
	$areaorg=~ s/ //g;

	if ($getgroup) {
		if ($areaorg=~ m/$getcity/ and $num eq $getgroup) {
			$buf.="<Result><Area>$area1 $area2 $area3</Area><PowerOutTime>${$Groups[$idx_1]}[$num]</PowerOutTime><PowerOutTime>${$Groups[$idx_2]}[$num]</PowerOutTime><PowerOutTime>${$Groups[$idx_3]}[$num]</PowerOutTime><Group>${num}</Group></Result>";
			++$count;
		}
	} else {
		if ($areaorg=~ m/$getcity/) {
			$buf.="<Result><Area>$area1 $area2 $area3</Area><PowerOutTime>${$Groups[$idx_1]}[$num]</PowerOutTime><PowerOutTime>${$Groups[$idx_2]}[$num]</PowerOutTime><PowerOutTime>${$Groups[$idx_3]}[$num]</PowerOutTime><Group>${num}</Group></Result>";
			++$count;
		}
	}
}

if (!$count) {
	$buf="<Result><Message>計画停電のないエリアとおもわれます。もしかすると地域名が狭すぎるかもしれません。もう少し広い地域名で検索することをおすすめします。</Message></Result>";
}
if ($count>400) {
	$buf="<Result><Message>地域名が広過ぎます。もう少し狭い地域名を入力してください。</Message></Result>";
}

print "Content-type: text/xml\n\n";
print qq!<?xml version="1.0" encoding="utf-8" ?>\n<ResultSet DataVersion="V.1.112" ResultRows="$count" >$buf</ResultSet>!;
