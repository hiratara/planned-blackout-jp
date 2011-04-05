use strict;
use warnings;
use lib qw(t/lib);
use File::Basename qw/dirname/;
use Plack::App::Directory;
use PlannedBlackoutJP::TestUtil qw/cgi_to_psgi/;

my $doc_root = (dirname __FILE__) . "/webapp";
my $dir = Plack::App::Directory->new({
    root => $doc_root
})->to_app;

my $app = sub {
    my $env = shift;
    if ($env->{PATH_INFO} =~ /\.cgi\b/) {
        my $psgi = cgi_to_psgi "$doc_root/$env->{PATH_INFO}";
        return $psgi->($env);
    } else {
        return $dir->($env);
    }
};
