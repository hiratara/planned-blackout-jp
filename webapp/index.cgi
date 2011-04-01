#!/usr/bin/perl

########################
# history of updates
# 2011/3/13 23:43 V1.001 indexpc.htmlの表示抑制対応 (tnx:nanakochi123456)
# 2011/3/13 23:17 initial release(mnakajim tnx:nanakochi123456)


use strict;
use warnings;

use File::Basename qw/dirname/;
BEGIN { require (dirname(__FILE__) . "/fatlib.pl") }
use PlannedBlackoutJP::Util qw/is_galapagos/;

my $location='indexpc.html';

if(is_galapagos \%ENV) {
	$location='indexm.html';
}

print "Content-type: text/html;charset=utf-8\n\n";

open my $fh, '<:utf8', $location;

while (<$fh>) {
	s/<meta http-equiv="refresh" content=".*$//;
	print;
}
