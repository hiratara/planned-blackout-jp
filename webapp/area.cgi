#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use FindBin qw($Bin);
BEGIN { require "$Bin/fatlib.pl" }
use Encode qw/decode_utf8/;
use Encode::Guess;
use CGI;
use PlannedBlackoutJP;
use PlannedBlackoutJP::Util qw/is_galapagos/;
use Text::MicroTemplate::File;
use constant DAY_SECONDS => 24 * 60 * 60;

binmode STDOUT, ":utf8";

sub date_str($) {
	my $time = shift;
	my ($d, $m, $y) = (localtime $time)[3, 4, 5];
	sprintf '%04d-%02d-%02d', $y + 1900, $m + 1, $d;
}

sub read_timetable() {
	my %timetable;

	open my $fh, '<:utf8', "$Bin/timetable.txt" or die $!;
	while (<$fh>) {
		my ($firm, $date, $group, @hours) = split /\t/, $_;
		next if $firm eq 'V'; # skip version line
		$timetable{$firm}{$date}{$group} = \@hours;
	}
	close $fh;

	return \%timetable;
}

sub read_runtable() {
	my %runtable;

	open my $fh, '<:utf8', "$Bin/runtable.txt" or die $!;
	while (<$fh>) {
		chomp;
		my ($date, $group, $state) = split /\t/, $_;
		$runtable{$date}{$group} = $state;
	}
	close $fh;

	return \%runtable;
}

sub search_zip($) {
	my $zip = shift;  # assumes that $zip has no hyphens.

	my @cities;
	open my $fh, '<:utf8', "$Bin/yubin.csv" or die $!;
	while (<$fh>) {
		chomp;
		my ($cur_zip, $left) = split /\t/, $_, 2;
		if ($zip == $cur_zip) {
			$left =~ tr/\t//d;
			push @cities, $left;
		}
	}
	close $fh;

	return @cities;
}

sub send_response($$$) {
	my ($query, $template, $args) = @_;

	my $mtf = Text::MicroTemplate::File->new(
		tag_start => '<%', tag_end => '%>', line_start => '%',
	);
	print $query->header("text/html; charset=utf-8");
	print $mtf->render_file($template, $args);
}

sub force_decode($) {
	my $str = shift;
	my $enc = guess_encoding($str, qw/shiftjis utf8/);
	return ref $enc ? $enc->decode($str) : decode_utf8($str);
}

sub addnor($) {
	my $add = shift;
	$add =~ tr/0-9がケヶのノ　 /０-９ケケケのの/d;

	# remove '字' and '大字'
	$add =~ s/([市区町村])大?字/$1/;

	return $add;
}

sub gettimetablever{
	open my $in, '<:utf8', "$Bin/timetable.txt" or die $!;
	while(<$in>) {
		chomp;
		my ($firm,$ver)=split(/\t/,$_);
		if($firm eq "V") {
			return $ver;
		}
	}
	return '--';
}

sub getareatablever{
	open my $in, '<:utf8', "$Bin/all.all" or die $!;
	while (<$in>) {
		chomp;
		my ($field,$ver)=split(/\t/,$_);
		if($field eq "version") {
			return $ver;
		}
	}
	return '--';
}

my $query=new CGI;
my $comm = $query->param('comm') || '';
my $view = $query->param('view') || (is_galapagos(\%ENV) ? 'm' : 'p');
my $criteria = do {
    my ($city) = grep {$_ ne ''} $query->param('city');  # choice one
    $city = '' unless defined $city;
    force_decode($city);
};
my $titlename = $criteria;
my $template = $view eq 'm' ? 'aream.html' : 'areapc.html';

my @dates = map {date_str(time + DAY_SECONDS * $_)} 0 .. 2;

my $regex_city;
if ($criteria =~ /^(\d{3})-?(\d{4})$/) {
	# called by zip code
	my $zipcode = "$1$2";
	my @cities = search_zip $zipcode;

	unless (@cities) {
		send_response $query, "$Bin/$template", {
			title => $titlename, dates => \@dates,
			areas => [], schedule_map => {}, 
			error_message => qq/郵便番号"$zipcode"は見つかりませんでした。/,
		};
		exit;
	}

	$regex_city = join '|', map { quotemeta(addnor $_) } @cities;
} else {
	$regex_city = addnor $criteria;
}

my $getgroup = $query->param('gid') || '';
$getgroup = '' unless $getgroup =~/^[1-5]$/;
my $getgroup_sub = $query->param('gids') || '';
$getgroup_sub = '' unless $getgroup_sub =~/^[A-E]$/;

my $auth='mnakajim';

if ($comm=~ m/ver/gi) {
	my $timetable = gettimetablever();
	my $areatable = getareatablever();
	print $query->header("text/plain");
	print "area.cgi : $PlannedBlackoutJP::VERSION($auth)\n";
	print "timetable.txt : $timetable\n";
	print "areatable.txt : $areatable\n";
	exit;
}



my $runtable = read_runtable;
my $timetable = read_timetable;

my @areas;
# {date => {area_id => {hours_str => '', run_str => '', }, ...}, ...}
my %schedule_map;
open my $in, '<:utf8', "$Bin/all.all" or die $!;
while (<$in>) {
	chomp;
	my ($area1,$area2,$area3,$num,$grp)=split (/\t/,$_);
	my $firm = 'T';  # XXX 東電。現状の実装では固定。

	next if $area1 eq 'version';

	my $areaorg = addnor "$area1$area2$area3";

	next if $getgroup && $num != $getgroup;
	next if $getgroup_sub && $grp ne $getgroup_sub;
	next if $regex_city && $areaorg !~ m/$regex_city/;

	my $area_id = @areas + 1;  # sequensial number
	push @areas, {
		id => $area_id,
		tdfk => $area1, 
		shiku => $area2, 
		machiaza => $area3,
		num => $num, grp => $grp,
	};

	for my $date (@dates) {
		my $hours = $timetable->{$firm}{$date}{$num};
		my $run_str = $runtable->{$date}{"$num\-$grp"} || '-';
		my $hours_str = $hours ? join(', ', @$hours) : '-';

		$schedule_map{$date}{$area_id} = {
			hours_str => $hours_str, run_str => $run_str
		};
	};
}
close $in;

my $error_message;
if (! @areas) {
	$error_message = "計画停電のないエリアです。";
} elsif (@areas > 400) {
	$error_message = "該当地域が多すぎです。詳細の地域名を入力してください。";
}

send_response $query, "$Bin/$template", {
	title => $titlename, 
	dates => \@dates, 
	areas => \@areas, 
	schedule_map => \%schedule_map, 
	error_message => $error_message,
};
