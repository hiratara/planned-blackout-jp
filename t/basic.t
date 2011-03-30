use strict;
use warnings;
use Test::More;
use File::Basename;
use Plack::App::WrapCGI;
use Test::WWW::Mechanize::PSGI;

chdir(dirname(__FILE__) . "/../webapp");

for (qw(index.cgi area.cgi)) {
    my $cgi = Plack::App::WrapCGI->new(
        script => "./$_", execute => 1,
    )->to_app;

    my $mech = Test::WWW::Mechanize::PSGI->new(app => $cgi);
    $mech->get_ok("/");
    ok $mech->content, "shouldn't be empty";
}

done_testing;
