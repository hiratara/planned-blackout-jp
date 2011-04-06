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

    # ken_all.csv should be broken. Too bad :(
    return if $machi =~ /\）/ && $machi !~ /\（/;

    $machi = '' if $machi =~ /(階|地階・階層不明)\）$/;  # buildings.
    $machi = '' if $machi eq '以下に掲載がない場合';
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

__END__

=encoding utf8

=head1 NAME

create_yubin_csv.pl - yubin.csv の作成

=head1 SYNOPSIS

  $ helper/create_yubin_csv.pl

=head1 DESCRIPTION

郵政省のホームページからデータを取得し、webapp/yubin.csv を作成する。

実行にはlha(http://lha.sourceforge.jp/)を必要とする。

=head1 PRINCIPLE

郵政省の提供するken_all.csv より、以下の方針で必要なデータを抽出する。
最終的に、「郵便場号7桁、都道府県、市区、町字」を列とするTSVを出力する。

  - 計画停電の対象である都道府県の郵便番号のみを選択する
  - ビル名称は無視し、町字を空とする
  - "以下に掲載がない場合"は無視し、町字を空とする
  - 住所末尾の"（...）"は無視し、取り除く

これらの動作により、郵便番号に紐づく住所はken_all.csvの記述が実際に意図する
地域よりも広い地域となる。

例:

  ・ken_all.csvの〒150-6001の住所
  　東京都渋谷区恵比寿恵比寿ガーデンプレイス（１階）
  ↓
  ・yubin.csvの〒150-6001の住所
  　東京都渋谷区

  ・ken_all.csvの〒171-0014の住所
  　東京都豊島区池袋（２〜４丁目）
  ↓
  ・yubin.csvの〒171-0014の住所
  　東京都豊島区池袋

=cut

