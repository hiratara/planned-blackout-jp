use strict;
use warnings;
use lib qw(t/lib lib);
use Test::More;
use File::Basename qw/dirname/;
use File::Temp qw/tempdir/;
use Test::WWW::Mechanize::PSGI;
use PlannedBlackoutJP::TestUtil qw/cgi_to_psgi dircopy rewrite_shebang/;

my $doc_root = dirname(__FILE__) . "/../webapp";
my $sample_dir = dirname(__FILE__) . "/../sample_data";
my $testdir = tempdir CLEANUP => 1;
dircopy($doc_root => $testdir);
dircopy($sample_dir => $testdir);
rewrite_shebang $testdir;

for (qw(index.cgi area.cgi)) {
    my $psgi = cgi_to_psgi "$testdir/$_";

    my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);
    $mech->get_ok("/");
    ok $mech->content, "shouldn't be empty";
}

done_testing;
