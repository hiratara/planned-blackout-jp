use strict;
use warnings;
use lib qw(t/lib lib);
use Test::More;
use Test::TCP;
use File::Basename qw/dirname/;
use File::Temp qw/tempdir/;
use Plack::Loader;
use Test::WWW::Mechanize::PSGI;
use PlannedBlackoutJP::TestUtil  qw/cgi_to_psgi dircopy rewrite_shebang/;

# A quick hack to stop "Wide character in print" warnings.
binmode $Test::Builder::Test->$_, ':utf8' 
                                     for qw/output todo_output failure_output/;

my $doc_root = dirname(__FILE__) . "/../webapp";
my $testdir = tempdir CLEANUP => 1;
dircopy($doc_root => $testdir);
rewrite_shebang $testdir;

# remove data file
unlink "$testdir/all.all" or die $!;

test_tcp(
    server => sub {
        my $port = shift;
        Plack::Loader->auto(port => $port)->run(sub {
            [200, [], ["OK\n"]]
        });
    },
    client => sub {
        my $port = shift;

        local $ENV{BLACKOUT_MASTER_URL} = "http://localhost:$port";

        my $psgi = cgi_to_psgi "$testdir/mirror_data.cgi";
        my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);
        $mech->get_ok("/");
        diag $mech->content;

        is do {local $/; open my $in, "$testdir/all.all"; <$in>}, "OK\n"
    },
);

done_testing;
