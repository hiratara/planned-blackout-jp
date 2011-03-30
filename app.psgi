use strict;
use warnings;
use File::Basename;
use Plack::App::Directory;
use Plack::App::WrapCGI;

require 't/util.pl';

my $doc_root = (dirname __FILE__) . "/webapp";
my $dir = Plack::App::Directory->new({
    root => $doc_root
})->to_app;

my $app = sub {
    my $env = shift;
    if ($env->{PATH_INFO} =~ /\.cgi\b/) {
        my $psgi = cgi_to_psgi("$doc_root/$env->{PATH_INFO}");
        return $psgi->($env);
    } else {
        return $dir->($env);
    }
};
