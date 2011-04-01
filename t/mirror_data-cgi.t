use strict;
use warnings;
use lib qw(t/lib lib);
use LWP::Simple qw/get/;
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

my @test_files = qw/all.all runtable.txt timetable.txt/;
my $doc_root = dirname(__FILE__) . "/../webapp";
my $testdir = tempdir CLEANUP => 1;
dircopy($doc_root => $testdir);
rewrite_shebang $testdir;

my %content_caches;
my $has_new_content = sub {
    my $file = shift;
    my $content = do {local $/; open my $in, "$testdir/$file"; <$in>};
    return defined $content && ! $content_caches{$content}++;
};

test_tcp(
    server => sub {
        my $port = shift;
        my $res = 200;
        my $access_cnt = 0;
        Plack::Loader->auto(port => $port)->run(sub {
            my $env = shift;
            if ($env->{PATH_INFO} =~ m#^/change_response/(\d{3})#) {
                $res = $1;
            }
            if ($res eq '304') {
                return ['304', ["Content-Length", "0"], []];
            } else {
                return [
                    $res, 
                    ["Content-Type", "text/plain"], 
                    ["ALL", ++$access_cnt, "\n"]
                ];
            }
        });
    },
    client => sub {
        my $port = shift;

        local $ENV{BLACKOUT_MASTER_URL} = "http://localhost:$port";

        my $psgi = cgi_to_psgi "$testdir/mirror_data.cgi";
        my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);

        # remove all data files
        unlink "$testdir/$_" for @test_files;

        $mech->get_ok("/");
        $mech->content_like(qr/^OK/);
        ok $has_new_content->($_) for @test_files;

        $mech->get_ok("/");
        $mech->content_like(qr/^ERROR/, "shouldn't crawl so frequently");
        ok ! $has_new_content->($_) for @test_files;

        # go back into the past
        my $long_long_ago = time - 60 * 60 * 24 * 365;
        utime $long_long_ago, $long_long_ago, "$testdir/$_" for @test_files;

        $mech->get_ok("/");
        $mech->content_like(qr/^OK/);
        ok $has_new_content->($_) for @test_files;

        # change the contents server status by sending HTTP request
        get("http://localhost:$port/change_response/304");
        utime $long_long_ago, $long_long_ago, "$testdir/$_" for @test_files;

        $mech->get_ok("/");
        $mech->content_like(qr/^OK/);
        ok ! $has_new_content->($_) for @test_files;
    },
);

done_testing;
