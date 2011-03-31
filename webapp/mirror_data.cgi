#!/usr/bin/perl
use strict;
use warnings;
use File::Basename qw/dirname/;
BEGIN { require (dirname(__FILE__) . "/fatlib.pl") }
use CGI;
use File::Basename qw/dirname/;
use HTTP::Tiny;

my @files = qw(all.all runtable.txt timetable.txt);
my $base_url = "http://bizoole.com/power";
my $base_dir = dirname(__FILE__);
my $interval = 60 * 60 * 30;  # 30 minutes

sub main($) {
    my $cgi = shift;
    my (@logs, @errors);

    my $http = HTTP::Tiny->new;
    for my $f (@files) {
        my $mtime = (stat "$base_dir/$f")[9] || 0;
        my $left_to_nexttime = $mtime + $interval - time;
        if ($left_to_nexttime > 0 ) {
            push @errors, "次の$fの確認まで、後$left_to_nexttime秒";
            next;
        }

        my $response = eval { $http->mirror("$base_url/$f", "$base_dir/$f") };
        if ($@) {
            my $error = $@;
            push @errors, $@;
            next;
        }

        if ($response->{status} eq '200') {
            push @logs, "$fを更新";
        } elsif ($response->{status} eq '304') {
            push @logs, "$fは最新";
        } else {
            push @errors, "$fの更新に失敗(Status=$response->{status})";
            next;
        }

        # XXX force touch and avoid loading too frequently.
        utime time, time, "$base_dir/$f";
    }

    my $body = @errors ? "ERROR\n\n" : "OK\n\n";
    return $body . (join '', map {$_, "\n"} @logs, @errors);
}

my $cgi = CGI->new;
my $body = eval { main $cgi };

print $cgi->header("text/plain; charset=UTF-8");
print $@ || $body;
