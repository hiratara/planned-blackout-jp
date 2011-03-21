#!/usr/bin/perl

$location='indexpc.html';

if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/) {
	$location='indexm.html';
}

print "Location:$location\n\n";
