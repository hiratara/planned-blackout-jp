use strict;

# カナ→ｶﾅ変換 from jcode.pl

sub z2h {
    my($s) = shift;
    my $re_euc_c    = '[\241-\376][\241-\376]';
    my $re_euc_kana = '\216[\241-\337]';
	from_to($s,'utf8','euc-jp');

	my %_H2Z = (
		 "\x8e\xa1"	=>	"\xa1\xa3",	#。
		 "\x8e\xa2"	=>	"\xa1\xd6",	#「
		 "\x8e\xa3"	=>	"\xa1\xd7",	#」
		 "\x8e\xa4"	=>	"\xa1\xa2",	#、
		 "\x8e\xa5"	=>	"\xa1\xa6",	#・
		 "\x8e\xa6"	=>	"\xa5\xf2",	#ヲ
		 "\x8e\xa7"	=>	"\xa5\xa1",	#ァ
		 "\x8e\xa8"	=>	"\xa5\xa3",	#ィ
		 "\x8e\xa9"	=>	"\xa5\xa5",	#ゥ
		 "\x8e\xaa"	=>	"\xa5\xa7",	#ェ
		 "\x8e\xab"	=>	"\xa5\xa9",	#ォ
		 "\x8e\xac"	=>	"\xa5\xe3",	#ャ
		 "\x8e\xad"	=>	"\xa5\xe5",	#ュ
		 "\x8e\xae"	=>	"\xa5\xe7",	#ョ
		 "\x8e\xaf"	=>	"\xa5\xc3",	#ッ
		 "\x8e\xb0"	=>	"\xa1\xbc",	#ー
		 "\x8e\xb1"	=>	"\xa5\xa2",	#ア
		 "\x8e\xb2"	=>	"\xa5\xa4",	#イ
		 "\x8e\xb3"	=>	"\xa5\xa6",	#ウ
		 "\x8e\xb4"	=>	"\xa5\xa8",	#エ
		 "\x8e\xb5"	=>	"\xa5\xaa",	#オ
		 "\x8e\xb6"	=>	"\xa5\xab",	#カ
		 "\x8e\xb7"	=>	"\xa5\xad",	#キ
		 "\x8e\xb8"	=>	"\xa5\xaf",	#ク
		 "\x8e\xb9"	=>	"\xa5\xb1",	#ケ
		 "\x8e\xba"	=>	"\xa5\xb3",	#コ
		 "\x8e\xbb"	=>	"\xa5\xb5",	#サ
		 "\x8e\xbc"	=>	"\xa5\xb7",	#シ
		 "\x8e\xbd"	=>	"\xa5\xb9",	#ス
		 "\x8e\xbe"	=>	"\xa5\xbb",	#セ
		 "\x8e\xbf"	=>	"\xa5\xbd",	#ソ
		 "\x8e\xc0"	=>	"\xa5\xbf",	#タ
		 "\x8e\xc1"	=>	"\xa5\xc1",	#チ
		 "\x8e\xc2"	=>	"\xa5\xc4",	#ツ
		 "\x8e\xc3"	=>	"\xa5\xc6",	#テ
		 "\x8e\xc4"	=>	"\xa5\xc8",	#ト
		 "\x8e\xc5"	=>	"\xa5\xca",	#ナ
		 "\x8e\xc6"	=>	"\xa5\xcb",	#ニ
		 "\x8e\xc7"	=>	"\xa5\xcc",	#ヌ
		 "\x8e\xc8"	=>	"\xa5\xcd",	#ネ
		 "\x8e\xc9"	=>	"\xa5\xce",	#ノ
		 "\x8e\xca"	=>	"\xa5\xcf",	#ハ
		 "\x8e\xcb"	=>	"\xa5\xd2",	#ヒ
		 "\x8e\xcc"	=>	"\xa5\xd5",	#フ
		 "\x8e\xcd"	=>	"\xa5\xd8",	#ヘ
		 "\x8e\xce"	=>	"\xa5\xdb",	#ホ
		 "\x8e\xcf"	=>	"\xa5\xde",	#マ
		 "\x8e\xd0"	=>	"\xa5\xdf",	#ミ
		 "\x8e\xd1"	=>	"\xa5\xe0",	#ム
		 "\x8e\xd2"	=>	"\xa5\xe1",	#メ
		 "\x8e\xd3"	=>	"\xa5\xe2",	#モ
		 "\x8e\xd4"	=>	"\xa5\xe4",	#ヤ
		 "\x8e\xd5"	=>	"\xa5\xe6",	#ユ
		 "\x8e\xd6"	=>	"\xa5\xe8",	#ヨ
		 "\x8e\xd7"	=>	"\xa5\xe9",	#ラ
		 "\x8e\xd8"	=>	"\xa5\xea",	#リ
		 "\x8e\xd9"	=>	"\xa5\xeb",	#ル
		 "\x8e\xda"	=>	"\xa5\xec",	#レ
		 "\x8e\xdb"	=>	"\xa5\xed",	#ロ
		 "\x8e\xdc"	=>	"\xa5\xef",	#ワ
		 "\x8e\xdd"	=>	"\xa5\xf3",	#ン
		 "\x8e\xde"	=>	"\xa1\xab",	#゛
		 "\x8e\xdf"	=>	"\xa1\xac",	#゜
	);

	my %_D2Z = (
		 "\x8e\xb6\x8e\xde"	=>	"\xa5\xac",	#ガ
		 "\x8e\xb7\x8e\xde"	=>	"\xa5\xae",	#ギ
		 "\x8e\xb8\x8e\xde"	=>	"\xa5\xb0",	#グ
		 "\x8e\xb9\x8e\xde"	=>	"\xa5\xb2",	#ゲ
		 "\x8e\xba\x8e\xde"	=>	"\xa5\xb4",	#ゴ
		 "\x8e\xbb\x8e\xde"	=>	"\xa5\xb6",	#ザ
		 "\x8e\xbc\x8e\xde"	=>	"\xa5\xb8",	#ジ
		 "\x8e\xbd\x8e\xde"	=>	"\xa5\xba",	#ズ
		 "\x8e\xbe\x8e\xde"	=>	"\xa5\xbc",	#ゼ
		 "\x8e\xbf\x8e\xde"	=>	"\xa5\xbe",	#ゾ
		 "\x8e\xc0\x8e\xde"	=>	"\xa5\xc0",	#ダ
		 "\x8e\xc1\x8e\xde"	=>	"\xa5\xc2",	#ヂ
		 "\x8e\xc2\x8e\xde"	=>	"\xa5\xc5",	#ヅ
		 "\x8e\xc3\x8e\xde"	=>	"\xa5\xc7",	#デ
		 "\x8e\xc4\x8e\xde"	=>	"\xa5\xc9",	#ド
		 "\x8e\xca\x8e\xde"	=>	"\xa5\xd0",	#バ
		 "\x8e\xcb\x8e\xde"	=>	"\xa5\xd3",	#ビ
		 "\x8e\xcc\x8e\xde"	=>	"\xa5\xd6",	#ブ
		 "\x8e\xcd\x8e\xde"	=>	"\xa5\xd9",	#ベ
		 "\x8e\xce\x8e\xde"	=>	"\xa5\xdc",	#ボ
		 "\x8e\xca\x8e\xdf"	=>	"\xa5\xd1",	#パ
		 "\x8e\xcb\x8e\xdf"	=>	"\xa5\xd4",	#ピ
		 "\x8e\xcc\x8e\xdf"	=>	"\xa5\xd7",	#プ
		 "\x8e\xcd\x8e\xdf"	=>	"\xa5\xda",	#ペ
		 "\x8e\xce\x8e\xdf"	=>	"\xa5\xdd",	#ポ
		 "\x8e\xb3\x8e\xde"     =>      "\xa5\xf4",     #ヴ
	);
	my %_Z2H = reverse %_H2Z;
	my %_Z2D = reverse %_D2Z;

    my $n = (
	     $s =~ s(
			  ($re_euc_c|$re_euc_kana)
			  ){
		 $_Z2D{$1} || $_Z2H{$1} || $1;
		 }eogx
	     );
	from_to($s,'euc-jp','utf8');
    $s;
}

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
