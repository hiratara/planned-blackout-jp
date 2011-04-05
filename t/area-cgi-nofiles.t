use strict;
use warnings;
use utf8;
use lib qw(t/lib lib);
use Test::More;
use File::Basename qw/dirname/;
use File::Temp qw/tempdir/;
use Test::WWW::Mechanize::PSGI;
use PlannedBlackoutJP::TestUtil  qw/
    cgi_to_psgi dircopy create_file date_str rewrite_shebang
/;

# A quick hack to stop "Wide character in print" warnings.
binmode $Test::Builder::Test->$_, ':utf8'
                                      for qw/output todo_output failure_output/;

my $doc_root = dirname(__FILE__) . "/../webapp";
my $sample_dir = dirname(__FILE__) . "/../sample_data";
my $testdir = tempdir CLEANUP => 1;
dircopy($doc_root => $testdir);
dircopy($sample_dir => $testdir);
rewrite_shebang $testdir;

my $psgi = cgi_to_psgi "$testdir/area.cgi";
my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);

for (qw/all.all runtable.txt timetable.txt/) {
    my $path = "$testdir/$_";
    rename $path, "$path.bk" or die $!;

    $mech->get_ok("/");
    ok $mech->content, "shouldn't be empty";

    rename "$path.bk", $path or die $!;
}

done_testing;
