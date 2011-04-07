#!/usr/bin/perl
# update cgi by nanakochi123456
# 2011/04/01 çXêVÇµÇƒÇ¢Ç‹Ç∑ÅB

$WGET="wget";
$BASEURL="http://power.daiba.cx/";
$BASEHTML="index.cgi";
$TMPDIR="/tmp/power_tmp";
$COUNTERDIR="counter";
$TAR="tar";
$CP="cp";
$RM="rm";
$BASEFILE="power";

print <<EOM;
Content-type: text/plain

Update from $BASEURL
EOM

$PWD = `pwd`;
chomp $PWD;
print "Current Dir: $PWD\n";

&shell("$RM -rf $TMPDIR");

print "mkdir&chdir $TMPDIR\n";
&shell("mkdir $TMPDIR");
if(opendir(DIR,"$TMPDIR")) {
	chdir("$TMPDIR");
	closedir(DIR);
} else {
	print "Cant make dir: $TMPDIR\n";
	exit;
}

print "Start...from $BASEURL\n";

open(PIPE,"$WGET -q $BASEURL/$BASEHTML|");
@DMY=<PIPE>;
close(PIPE);
close(PIPE);

$BASEURLREGEX=$BASEURL;
$BASEURLREGEX=~s/\:/\\:/g;
$BASEURLREGEX=~s/\//\\\//g;
$BASEURLREGEX=~s/\./\\\./g;

if(open(R,"$BASEHTML")) {
	foreach(<R>) {
		if(/$BASEURLREGEX$BASEFILE(.+)\.tar\.gz\"/) {
			$VERSION=$1;
			last;
		}
	}
	close(R);
} else {
	print "$BASEHTML not found\n";
	exit;
}

print "Version: $VERSION\n";
print "Get $BASEURL$BASEFILE$VERSION.tar.gz\n";
open(PIPE,"$WGET -q $BASEURL/$BASEFILE$VERSION.tar.gz|");
@DMY=<PIPE>;
close(PIPE);
if(-r "$BASEFILE$VERSION.tar.gz") {
	print "Extract: $BASEFILE$VERSION.tar.gz\n";
	if(open(PIPE,"$TAR xvfz $BASEFILE$VERSION.tar.gz 1>/dev/null 2>/dev/null|")) {
		@DMY=<PIPE>;
		close(PIPE);
	} else {
		print "$TAR xvfz $BASEFILE$VERSION.tar.gz can't extract";
		exit;
	}
} else {
	print "$BASEFILE$VERSION.tar.gz not found\n";
	exit;
}

chdir("$PWD");
print "Dir check: $TMPDIR/$BASEFILE$VERSION\n";
if(opendir(DIR,"$TMPDIR/$BASEFILE$VERSION")) {
	while($file=readdir(DIR)) {
		next if($file eq '.' || $file eq '..');
		next if($file eq $COUNTERDIR);
		print "copy $TMPDIR/$BASEFILE$VERSION/$file $PWD/$file\n";
		&filecopy("$TMPDIR/$BASEFILE$VERSION/$file","$PWD/$file");
	}
	closedir(DIR);
	&shell("$RM -rf $TMPDIR");

	if(-r "$PWD/.htaccess.org") {
		print "Found $PWD/.htaccess.org\n";
		&filecopy("$PWD/.htaccess.org","$PWD/.htaccess");
		print "copy $PWD/.htaccess.org $PWD/.htaccess\n";
	}
	print "mkdir&chmod $PWD/$COUNTERDIR\n";
	&shell("mkdir $PWD/$COUNTERDIR\n");
	&shell("chmod 755 $PWD/$COUNTERDIR\n");

	print "Complete.\n";
	exit;
} else {
	print "$TMPDIR/$BASEFILE$VERSION can't read\n";
	exit;
}

sub filecopy {
	my($old,$new)=@_;

	&shell("$CP $old $new");
	if($new=~/\.cgi/) {
		chmod(oct(755),$new);
	} else {
		chmod(oct(644),$new);
	}
}

sub shell {
	my($shell)=@_;
	open(PIPE,"$shell|");
	foreach(<PIPE>) {
		chomp;
	}
	close(PIPE);
}
