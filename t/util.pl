use strict;
use warnings;
use File::Basename qw/dirname/;
use File::Copy qw/cp/;
use File::Find qw/find/;
use File::Spec;
use Cwd qw/getcwd/;

sub cgi_to_psgi {
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

sub dircopy {
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

sub create_file {
    my ($path, $content) = @_;
    open my $out, '>:utf8', $path or die "$!: $path";
    print $out $content;
}

sub date_str {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

1;
