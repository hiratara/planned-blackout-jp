use strict;
use warnings;
use Cwd qw/getcwd/;
use File::Basename;
use File::Spec;
use Plack::App::Directory;
use Plack::App::WrapCGI;

sub exec_in_dir(&$) {
    my ($code, $dir) = @_;

    my $cur_dir = getcwd;
    my $ret = eval {
        chdir $dir;
        $code->();
    };
    chdir $cur_dir;
    $@ and die $@;

    return $ret;
}

my $doc_root = File::Spec->rel2abs((dirname __FILE__) . "/webapp");
my $dir = Plack::App::Directory->new({
    root => $doc_root
})->to_app;

my $app = sub {
    my $env = shift;
    if ($env->{PATH_INFO} =~ /\.cgi\b/) {
        my $cgi = Plack::App::WrapCGI->new(
            script => "$doc_root/$env->{PATH_INFO}", 
            execute => 1
        )->to_app;
        return exec_in_dir {$cgi->($env)} $doc_root;
    } else {
        return $dir->($env);
    }
};
