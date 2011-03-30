use strict;
use warnings;
use Test::More;
use File::Basename;
use Plack::App::WrapCGI;
use Test::WWW::Mechanize::PSGI;

my $dir = (dirname __FILE__) . "/../webapp";

my $cgi = Plack::App::WrapCGI->new(
    script => "$dir/area.cgi", execute => 1,
)->to_app;
my $mech = Test::WWW::Mechanize::PSGI->new(app => $cgi);

$mech->get_ok("/");

done_testing;
