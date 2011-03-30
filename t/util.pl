use strict;
use warnings;
use File::Basename qw/dirname/;
use File::Spec;
use Cwd qw/getcwd/;

sub cgi_to_psgi {
    my $cgi = shift;
    my $abs_path = File::Spec->rel2abs($cgi);
    my $abs_dir = dirname $abs_path;

    my $psgi = Plack::App::WrapCGI->new(
        script => $abs_path, execute => 1
    )->to_app;

    sub {
        my $env = shift;

        my $cur_dir = getcwd;
        my $res = eval {
            chdir $abs_dir;
            $psgi->($env);
        };
        chdir $cur_dir;
        $@ and die $@;

        return $res;
    };
}

1;
