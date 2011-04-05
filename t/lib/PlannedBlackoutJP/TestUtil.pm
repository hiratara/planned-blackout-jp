package PlannedBlackoutJP::TestUtil;

use strict;
use warnings;
use File::Basename qw/dirname/;
use File::Copy qw/cp/;
use File::Find qw/find/;
use File::Spec;
use Cwd qw/getcwd/;
use Exporter qw/import/;
use Plack::App::WrapCGI;

our @EXPORT = qw/cgi_to_psgi dircopy create_file date_str rewrite_shebang/;

sub cgi_to_psgi($) {
    my $cgi = shift;
    my $abs_path = File::Spec->rel2abs($cgi);
    my $abs_dir = dirname $abs_path;

    my $psgi = Plack::App::WrapCGI->new(
        script => $abs_path, execute => 1
    )->to_app;

    sub {
        my $env = shift;

        my $cur_dir = getcwd;
        my $res = eval {
            chdir $abs_dir;
            $psgi->($env);
        };
        chdir $cur_dir;
        $@ and die $@;

        return $res;
    };
}

sub dircopy($$) {
    my ($dir_from, $dir_to) = @_;
    s{/$}{} for $dir_from, $dir_to;

    find sub {
        /^\.+$/ and return;

        (my $path_to = $File::Find::name) =~ s{^\Q$dir_from\E(/|$)}{$dir_to$1};

        if (-d) {
            mkdir $path_to or die "$!: $path_to";
        } else {
            cp $_, $path_to or die "$!: $_ => $path_to";
        }
    }, $dir_from;
}

sub create_file($$) {
    my ($path, $content) = @_;
    open my $out, '>:utf8', $path or die "$!: $path";
    print $out $content;
}

sub rewrite_shebang($;$) {
    my ($root_dir, $perl_exec) = @_;
    $perl_exec ||= $ENV{BLACKOUT_PERLEXEC};

    return unless defined $perl_exec;
    -x $perl_exec or die "invalid exec: $perl_exec";

    find sub {
        /^\.+$/ and return;
        -f && -x or return;

        open my $in, '<:utf8', $_ or die $!;
        (my $shebang_line = <$in>) =~ /\bperl\b/ or return;
        my $left_part = do {local $/; <$in>};
        close $in;

        create_file $_ => "#!$perl_exec\n$left_part";
    }, $root_dir;
}

sub date_str($) {
    my $time = shift;
    my ($d, $m, $y) = (localtime $time)[3, 4, 5];
    sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

1;

__END__

=head1 NAME

PlannedBlackoutJP::TestUtil - Utilities for tests.

=cut

