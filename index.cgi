#!/usr/bin/perl

########################
# history of updates
# 2011/3/13 23:43 V1.001 indexpc.htmlの表示抑制対応 (tnx:nanakochi123456)
# 2011/3/13 23:17 initial release(mnakajim tnx:nanakochi123456)

$location='indexpc.html';

if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/) {
	$location='indexm.html';
}

print "Content-type: text/html;charset=utf-8\n\n";

open (READ,$location);

while (<READ>) {
	s/<meta http-equiv="refresh" content=".*$//;
	print;
}
