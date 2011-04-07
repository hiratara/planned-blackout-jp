# QUERY_STRINGエンコード - これも面倒だからpyukiwikiから移植
sub encode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}

# $basehref, $basepath 取得 - これも面倒だからpyukiwikiから移植
sub getbasehref {
	# Thanks moriyoshi koizumi.
	$basehost = "$ENV{'HTTP_HOST'}";
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
	$basepath=$uri;
	$basepath=~s/\/[^\/]*$//g;
	$basehref=$basehost . $uri;
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

	if($mode eq 'result') {
		$defaultECC='M';
		$defaultVersion=15;
		$defaultSize=3;
	} else {
		$defaultECC='M';
		$defaultVersion=5;
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
