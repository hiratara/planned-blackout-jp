package PlannedBlackoutJP::Util;
use strict;
use warnings;

use Exporter qw/import/;

our @EXPORT = qw/is_galapagos/;

sub is_galapagos($) {
    my $env = shift;
    return $env->{HTTP_USER_AGENT} =~ /
        DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|
        WILLCOM|iPod|PDA
    /x;
}

1;
