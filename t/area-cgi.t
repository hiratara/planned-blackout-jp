use strict;
use warnings;
use utf8;
use lib qw(t/lib lib);
use Test::More;
use Encode qw/encode encode_utf8/;
use File::Basename qw/dirname/;
use File::Temp qw/tempdir/;
use Plack::App::WrapCGI;
use Test::WWW::Mechanize::PSGI;
use PlannedBlackoutJP::TestUtil  qw/
    cgi_to_psgi dircopy create_file date_str rewrite_shebang
/;

# A quick hack to stop "Wide character in print" warnings.
binmode $Test::Builder::Test->output, ':utf8';

my $today = date_str(time);

my $doc_root = dirname(__FILE__) . "/../webapp";
my $testdir = tempdir CLEANUP => 1;
dircopy($doc_root => $testdir);
rewrite_shebang $testdir;

create_file("$testdir/all.all" => <<__TEXT__);
東京都	荒川区	町屋１丁目	5	B
神奈川県	横浜市港北区	大曽根２丁目	3	D
version	01/01 00:00
__TEXT__

create_file("$testdir/timetable.txt" => <<__TEXT__);
T	2000-01-01	3	12:20-16:00
T	$today	3	06:20-10:00	13:50-17:30
T	$today	5	12:20-16:00
V	2011-01-01
__TEXT__

create_file("$testdir/runtable.txt" => <<__TEXT__);
2000-01-01	3-D	中止
$today	3-D	実施予定
$today	5-B	中止
__TEXT__

my $psgi = cgi_to_psgi "$testdir/area.cgi";
my $mech = Test::WWW::Mechanize::PSGI->new(app => $psgi);

for (
    "city=" . encode_utf8 '港北区大曽根２丁目', 
    "city=" . encode_utf8 '2丁目', 
    "city=" . encode_utf8 '神奈川県　横浜市港北区　大曽根２丁目', 
    "city=" . encode('sjis', '港北区大曽根２丁目'), # for AU's cellphone
    "gid=3",
) {
    $mech->get_ok("/?$_");
    $mech->content_contains("大曽根２丁目");
    $mech->content_lacks("町屋１丁目");
    $mech->content_contains("13:50");
    $mech->content_lacks("12:20");
    $mech->content_contains("実施予定");
    $mech->content_lacks("中止");
}

$mech->get_ok("/");
$mech->content_lacks("第-グループ", "shouldn't have empty rows.");

$mech->get_ok("/?comm=ver");
$mech->content_like(qr/^[\w.\-]+\s*:\s*\w+\.\w+\(\w+\)$/sm);

done_testing;
