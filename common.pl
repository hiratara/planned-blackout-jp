use strict;

# QUERY_STRINGエンコード - これも面倒だからpyukiwikiから移植
sub encode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}

# $basehref, $basepath 取得 - これも面倒だからpyukiwikiから移植
sub getbasehref {
	# Thanks moriyoshi koizumi.
	my $basehost = "$ENV{'HTTP_HOST'}";
	$basehost = 'http://' . $basehost;
	# Special Thanks to gyo
	$basehost .= ":$ENV{'SERVER_PORT'}"
		if ($ENV{'SERVER_PORT'} ne '80' && $basehost !~ /:\d/);
	# URLの生成
	my $uri;
	my $req=$ENV{REQUEST_URI};
	$req=~s/\?.*//g;
	if($req ne '') {
		if($req eq $ENV{SCRIPT_NAME}) {
			$uri= $ENV{'SCRIPT_NAME'};
		} else {
			for(my $i=0; $i<length($ENV{SCRIPT_NAME}); $i++) {
				if(substr($ENV{SCRIPT_NAME},$i,1) eq substr($req,$i,1)) {
					$uri.=substr($ENV{SCRIPT_NAME},$i,1);
				} else {
					last;
				}
			}
		}
	} else {
		$uri .= $ENV{'SCRIPT_NAME'};
	}
	my $basepath=$uri;
	$basepath=~s/\/[^\/]*$//g;
	my $basehref=$basehost . $uri;
	return($basehref, $basehost, $basepath);
}

# gzip圧縮
sub gzip_compress {
	my $header=shift;
	my $gzip_command="gzip";
	my $gzip_path;
	my $gzip_header;
	my $fastflag;
	my $forceflag;
	foreach(split(/:/,$ENV{PATH})) {
		if(-x "$_/$gzip_command") {
			$gzip_path="$_/$gzip_command" ;
			if(open(PIPE,"$gzip_path --help 2>&1|")) {
				foreach(<PIPE>) {
					$forceflag="--force" if(/(\-\-force)/);
					$fastflag="--fast" if(/(\-\-fast)/);
				}
				close(PIPE);
			}
		}
	}
	$gzip_path="$gzip_path $fastflag $forceflag";
	if ($gzip_path ne '') {
		if(($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/)) {
			if($ENV{'HTTP_ACCEPT_ENCODING'}=~/x-gzip/) {
				$gzip_header="Content-Encoding: x-gzip\n";
			} else {
				$gzip_header="Content-Encoding: gzip\n";
			}
		}
	}

	# サーバー出力
	print "$header\n";
	print "$gzip_header" if($gzip_header ne '');
	print "\n";

	if ($gzip_header ne '') {
		open(STDOUT,"| $gzip_path");
		binmode(STDOUT);
	}
}

# use モジュールと同等、なくても動作するようになっています。
sub load_module{
	my $mod = shift;
	eval qq( require $mod; );
	unless($@) {
		return 1;
	} else {
		return 0;
	}
}

# QR code module from Pyukiwiki by nanakochi123456
# Base:http://pyukiwiki.sourceforge.jp/PyukiWiki/Plugin/Nanami/qrcode/

# QRコードの画像自体を作成
sub make_qrcode {
	my ($string,$mode) = @_;
	my %hParm;
	my $oGdBar;

	my $defaultECC;
	my $defaultVersion;
	my $defaultSize;

	if($mode eq 'result') {
		$defaultECC='M';
		$defaultVersion=15;
		$defaultSize=3;
	} else {
		$defaultECC='M';
		$defaultVersion=6;
		$defaultSize=3;
	}

	if(&load_module("GD::Barcode")) {
		$hParm{Ecc}=$defaultECC;
		$hParm{ModuleSize}=$defaultSize;
		$hParm{Version}=$defaultVersion;
		$oGdBar = GD::Barcode->new(
			'QRcode',
			$string,
			\%hParm);
		die($GD::Barcode::errStr) unless($oGdBar);

		binmode(STDOUT);
		print <<FIN;
Content-type: image/png

FIN
		print $oGdBar->plot->png;
		exit;
	}
}

1;
