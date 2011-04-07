#!/usr/bin/perl

use strict;

my $VER="V.1.202(nanakochi123456  1st release:mnakajim)";
my $tarball="power110402.tar.gz";
my $data_update=<<EOM;
<li>2011/4/01 20:24 東京電力データを更新。</li>
<li>2011/4/01 11:10 東京電力、２～４日計画停電なしに対応。</li>
<li>2011/3/31 19:55 東京電力データを更新。</li>
<li>2011/3/31 14:55 東京電力、１日計画停電実施なしに対応。対応遅くなり申し訳ありません。</li>
<li>2011/4/01 07:11 東北電力分の将来のデータが入っていなかったものを修正した。</li>
<li>2011/3/31 07:40 東京電力データを更新。</li>
<li>2011/3/30 13:35 東京電力、３１日計画停電実施なしに対応。</li>
<li>2011/3/30 08:53 東京電力データを更新。</li>
<li>2011/3/29 15:49 runtable.txtを正式採用した。</li>
<li>2011/3/29 14:00 東京電力、３０日計画停電実施なしに対応。</li>
<li>2011/3/28 20:33 東京電力データを更新。</li>
<li>2011/3/28 18:00 東京電力、２９日計画停電実施なしに対応。</li>
<li>2011/3/28 11:43 東京電力第４、５グループの実施なしに対応。</li>
<li>2011/3/28 06:06 twitter情報が完全でなかった為、ホームページより入手した情報を入力した。</li>
EOM

my $engine_update=<<EOM;
<li>2011/4/02 11:01 サブグループも含めた検索を実装した。携帯の出力を変更した。</li>
<li>2011/4/01 18:27 カウンターを実装してみました。ただし、カウンターの結果は comm=ver の時のみ出力されます。ユーザー権限がないサーバーでは、chmod 777 counter をするか、それをせずカウンターを動作させない方法があります。</li>
<li>2011/4/01 14:34 gdモジュール、またはGD.pmがなく、GD::Barcode.pmがある環境で正常になるようにした。</li>
<li>2011/3/31 08:10 モバイルでもエンジン及びデータの更新履歴を見れるようにした。</li>
<li>2011/3/29 15:49 runtable.txtを正式採用した。</li>
<li>2011/3/29 15:07 一部郵便番号で検索できなくなっていたのを修正した。</li>
<li>2011/3/29 13:00 runtable.txtから詳細情報を取得するようにした（α版）</li>
<li>2011/3/29 11:40 アイコンを付けてみました。ICON素材 by watanabe_haruna</li>
<li>2011/3/28 20:34 バージョン情報へのリンクを追加した。また、バージョン情報の表示時にQRコード及びRSSのリンクを出力しないようにした</li>
<li>2011/3/28 08:04 東京電力が速報で一部サブグループのみの実施となった場合に、きちんと計画停電を実施するかしないかを明確にできるようにした。</li>
EOM

#------------
use Encode qw/decode encode_utf8 from_to/;
require "common.pl";

$VER=~s/\(.*//g;
my $nojapaneseflg=0;
$nojapaneseflg=1 if($ENV{HTTP_ACCEPT_LANGUAGE}!~/ja/);
my $mobileflg=0;
$mobileflg=1 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/);

$mobileflg=0 if($ENV{QUERY_STRING}=~'p');
$mobileflg=1 if($ENV{QUERY_STRING}=~'m');
$nojapaneseflg=0 if($ENV{QUERY_STRING}=~'j');
$nojapaneseflg=1 if($ENV{QUERY_STRING}=~'e');

my $english_file="english.html";
my $english_mobile_file="english_mobile.html";
my $mobile_file="mobile.html";
my $pc_file="pc.html";
my $mobile_update_file="mobile_update.html";

&gzip_compress("Content-type: text/html; charset=utf-8");
my $body;
my $file;
my $kanaflg=0;
my $updatetitle;
if($nojapaneseflg) {
	if($mobileflg) {
		$file=$english_mobile_file;
	} else {
		$file=$english_file;
	}
} elsif($ENV{QUERY_STRING} eq 'mu') {
	$file=$mobile_update_file;
	$kanaflg=1;
} elsif($mobileflg) {
	$file=$mobile_file;
} else {
	$file=$pc_file;
}

if(open(R,$file)) {
	foreach(<R>) {
		if(/\@\@/) {
			s/\@\@VER\@\@/$VER/;
			s/\@\@INCLUDE\=\"(.+)\"\@\@/@{[&include($1)]}/;
			s/\@\@QRCODEEN\@\@/@{[&qrcode_link_en]}/;
			s/\@\@QRCODEJP\@\@/@{[&qrcode_link]}/;
			s/\@\@DATAUPDATE\@\@/$data_update/;
			s/\@\@ENGINEUPDATE\@\@/$engine_update/;
			s/\@\@TARBALL\@\@/$tarball/;
		}
		$body.=$_;
	}
	close(R);
} else {
	$body="$file not found. sorry.";
}
if($kanaflg) {
	$body=&z2h($body);
	$body=~s/０/0/g;
	$body=~s/１/1/g;
	$body=~s/２/2/g;
	$body=~s/３/3/g;
	$body=~s/４/4/g;
	$body=~s/５/5/g;
	$body=~s/６/6/g;
	$body=~s/７/7/g;
	$body=~s/８/8/g;
	$body=~s/９/9/g;
}
print "$body\n";
close(STDOUT);
exit;

sub include {
	my $file=shift;
	my $body="";
	if(open(I,$file)) {
		my $div=$file;
		$div=~s/\.//g;
		$body.=<<EOM;
<div id="$div">
EOM
		foreach(<I>) {
			$body.=$_;
		}
		close(I);
		$body.="</div>\n";
	}
	$body;
}

sub qrcode_link {
	my($basehref, $basehost, $basepath)=&getbasehref;
	my $string=&encode("$basehost$basepath");
	if(&load_module("GD") && &load_module("GD::Barcode")) {
		return <<FIN;
携帯へURLを送るには、こちらのQRコードをご利用下さい。<br />
<img alt="QRCode" src="$basehost$basepath/area.cgi?m=qr\&amp;str=$string" />

FIN
	}
	'';
}

sub qrcode_link_en {
	my($basehref, $basehost, $basepath)=&getbasehref;
	my $string=&encode("$basehost$basepath?e");
	if(&load_module("GD::Barcode")) {
		return <<FIN;
If you have mobile phone to transfer this site, use this barcode.
<br />
<img alt="QRCode" src="$basehost$basepath/area.cgi?m=qr\&amp;str=$string" />

FIN
	}
	'';
}

