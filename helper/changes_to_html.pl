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

print +(render_mt do {local $/; <DATA>}, \@histories)->as_string;

__END__
? for (@{$_[0]}) {
<li><?= $_->{date} ?> V<?= $_->{ver} ?>
  <ul>
?   for (@{$_->{logs}}) {
    <li><?= $_ ?></li>
?   }
  </ul>
</li>
? }
