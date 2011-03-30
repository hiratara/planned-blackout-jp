use strict;
use warnings;
use Test::More;
use File::Basename;
use Plack::App::WrapCGI;
use Test::WWW::Mechanize::PSGI;

require "t/util.pl";
my $doc_root = dirname(__FILE__) . "/../webapp";

for (qw(index.cgi area.cgi)) {
    my $psgi = cgi_to_psgi("$doc_root/$_");

    my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);
    $mech->get_ok("/");
    ok $mech->content, "shouldn't be empty";
}

done_testing;
