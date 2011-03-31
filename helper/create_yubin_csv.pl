#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Cwd qw/cwd/;
use File::Basename qw/dirname/;
use File::Find qw/find/;
use File::Temp qw/tempdir/;
use LWP::Simple qw/mirror/;

my $lzh_url = 'http://www.post.japanpost.jp/zipcode/dl/oogaki/lzh/ken_all.lzh';
my $lha_exe = 'lha';
my $output = (dirname __FILE__) . "/../webapp/yubin.csv";
my @tdfks = qw/埼玉県 神奈川県 静岡県 東京都 栃木県 群馬県 千葉県 山梨県/;

sub call_in_dir(&$) {
    my ($code, $dir) = @_;

    my $orig_dir = cwd;
    eval {
        chdir $dir or die $!;
        $code->();
    };
    chdir $orig_dir or die $!;

    $@ and die $@;
}

sub normalize_address($$$) {
    my ($tdfk, $shi, $machi) = @_;
    return if $machi eq '以下に掲載がない場合';
    return if $machi =~ /(階|次のビルを除く|地階・階層不明)\）$/;

    # ken_all.csv should be broken. Too bad :(
    return if $machi =~ /\）/ && $machi !~ /\（/;

    $machi =~ s/\（[^\）]+\）?$//;

    return $tdfk, $shi, $machi;
}

my $tmpdir = tempdir CLEANUP => 1;
my $lzh_file = "$tmpdir/ken_all.lzh";
my $code = mirror "$lzh_url", $lzh_file;

call_in_dir {
    system($lha_exe, '-x', $lzh_file) >> 8 == 0 or die $!;
} $tmpdir;

my $csv_file;
find sub {
    if (-f and /\.csv$/) {
        $csv_file = $File::Find::name;  # Overidden everytime.
        return;
    }
}, $tmpdir;

die "no csv file found" unless defined $csv_file;

my $tdfk_reg = "(" . (join '|', map { quotemeta $_ } @tdfks) . ")";
open my $in, '<:encoding(sjis)', $csv_file or die "$!: $csv_file";
open my $out, '>:utf8', $output or die "$!: $output";
while (<$in>) {
    /"$tdfk_reg"/ or next; # Drops first for performance

    my ($zip, $tdfk, $shi, $machi) = (
        map {tr/"//d; $_} split /,/, $_
    )[2, 6, 7, 8];

    ($tdfk, $shi, $machi) = normalize_address($tdfk, $shi, $machi);
    next unless defined $tdfk;

    print $out +(join "\t", $zip, $tdfk, $shi, $machi), "\n";
}
close $in;
close $out;
