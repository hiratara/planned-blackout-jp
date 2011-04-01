#!/usr/bin/perl

########################
# history of updates
# 2011/3/13 23:43 V1.001 indexpc.htmlの表示抑制対応 (tnx:nanakochi123456)
# 2011/3/13 23:17 initial release(mnakajim tnx:nanakochi123456)


use strict;
use warnings;
use File::Basename qw/dirname/;
BEGIN { require (dirname(__FILE__) . "/fatlib.pl") }
use CGI;
use PlannedBlackoutJP::Util qw/is_galapagos/;
use Text::MicroTemplate::File;

my $q = CGI->new;
my $view = $q->param('view') || (is_galapagos(\%ENV) ? 'm' : 'p');

my $template = $view eq 'm' ? 'indexm.html' : 'indexpc.html';

print $q->header("text/html;charset=utf-8");
my $mtf = Text::MicroTemplate::File->new(
    tag_start => '<%', tag_end => '%>', line_start => '%',
);
print $mtf->render_file($template, {version => '1.200'});
