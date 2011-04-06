#!/usr/bin/env perl
use strict;
use warnings;
use Text::MicroTemplate qw/render_mt/;

binmode STDOUT, ':utf8';

open my $in, '<:utf8', 'webapp/Changes' or die $!;
my @histories;
my $cur_slot;
while (<$in>) {
    chomp;
    if (my ($ver, $date) = m{^(\d(?:\.\d+\w*)+) (\d+/\d+/\d+ \d+:\d+)}) {
        # header line
        $cur_slot = {ver => $ver, date => $date};
        push @histories, $cur_slot;
    } elsif (/^\s+\-\s*(.+)$/) {
        push @{$cur_slot->{logs}}, $1;
    }
}

print +(render_mt <<'__TEMPLATE__', \@histories)->as_string;
? for (@{$_[0]}) {
<li><?= $_->{date} ?> V<?= $_->{ver} ?>
  <ul>
?   for (@{$_->{logs}}) {
    <li><?= $_ ?></li>
?   }
  </ul>
</li>
? }
__TEMPLATE__

__END__

=encoding utf8

=head1 NAME

changes_to_html.pl - Changesファイルの内容をhtml化する

=head1 SYNOPSIS

  $ helper/changes_to_html.pl > changes_lists.html

=head1 DESCRIPTION

Changesファイルの内容をパースし、<ul>...</ul>内に記述できるリスト形式の
htmlを標準出力へ出力する。

=cut

