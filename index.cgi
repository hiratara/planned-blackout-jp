#!/usr/bin/perl

use strict;

my $VER="V.1.200(nanakochi123456  1st release:mnakajim)";
my $tarball="power110331.tar.gz";
my $data_update=<<EOM;
<li>2011/3/31 07:40 東京電力データを更新。</li>
<li>2011/3/30 13:35 東京電力、３１日計画停電実施なしに対応。</li>
<li>2011/3/30 08:53 東京電力データを更新。</li>
<li>2011/3/29 15:49 runtable.txtを正式採用した。</li>
<li>2011/3/29 14:00 東京電力、３０日計画停電実施なしに対応。</li>
<li>2011/3/28 20:33 東京電力データを更新。</li>
<li>2011/3/28 18:00 東京電力、２９日計画停電実施なしに対応。</li>
<li>2011/3/28 11:43 東京電力第４、５グループの実施なしに対応。</li>
<li>2011/3/28 06:06 twitter情報が完全でなかった為、ホームページより入手した情報を入力した。</li>
<li>2011/3/27 22:07 東京電力のデータを更新した。またtwitter情報によりグループ２の詳細を入力した。</li>
<li>2011/3/27 12:54 東北電力のデータを更新した。なお省略部分がある為、市町村までの入力で一度検索してみて下さい。</li>
<li>2011/3/27 20:11 東京電力側のデータに欠損があった為、反映した。</li>
<li>2011/3/27 13:17 本家に対応しやすいように、all.allを変更した。</li>
<li>2011/3/26 09:17 東京電力3月26日更新データに更新した。東京都にもサブグループが付くようになります。</li>
<li>2011/3/26 03:16 東京電力２５グループ化に対応した。なお、東京都は現状ではデータがない為、今まで通りの表示となります。</li>
<li>2011/3/25 18:40 東京電力２６日、２７日実施なしに対応した。</li>
<li>2011/3/25 03:14 東京電力データを更新した。</li>
EOM

my $engine_update=<<EOM;
<li>2011/3/31 08:10 モバイルでもエンジン及びデータの更新履歴を見れるようにした。</li>
<li>2011/3/29 15:49 runtable.txtを正式採用した。</li>
<li>2011/3/29 15:07 一部郵便番号で検索できなくなっていたのを修正した。</li>
<li>2011/3/29 13:00 runtable.txtから詳細情報を取得するようにした（α版）</li>
<li>2011/3/29 11:40 アイコンを付けてみました。ICON素材 by watanabe_haruna</li>
<li>2011/3/28 20:34 バージョン情報へのリンクを追加した。また、バージョン情報の表示時にQRコード及びRSSのリンクを出力しないようにした</li>
<li>2011/3/28 08:04 東京電力が速報で一部サブグループのみの実施となった場合に、きちんと計画停電を実施するかしないかを明確にできるようにした。</li>
<li>2011/3/27 12:54 ローマ字でスペースが入っていると検索できないバグを直した。</li>
<li>2011/3/27 07:30 area.cgi?comm=ver の返り値を本家とほぼ同じにした。文字正規化方法を本家と同じにした。携帯版での色出力を抑制した(パケ代節約のため)</li>
<li>2011/3/25 13:16 本家に対応しやすいように、エンジンを変更した。</li>
<li>2011/3/25 18:40 東京電力のグループが 1-Aや、5-Cになるのを仮対応した。</li>
EOM

#------------
use Encode qw/decode encode_utf8 from_to/;
require "common.pl";

$VER=~s/\(.*//g;
my $nojapaneseflg=0;
$nojapaneseflg=1 if($ENV{HTTP_ACCEPT_LANGUAGE}!~/ja/);
my $mobileflg=0;
$mobileflg=1 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/);

$mobileflg=0 if($ENV{QUERY_STRING} eq 'p');
$mobileflg=1 if($ENV{QUERY_STRING} eq 'm');
$nojapaneseflg=0 if($ENV{QUERY_STRING} eq 'j');
$nojapaneseflg=1 if($ENV{QUERY_STRING} eq 'e');

my $english_file="english.html";
my $mobile_file="mobile.html";
my $pc_file="pc.html";
my $mobile_update_file="mobile_update.html";

&gzip_compress("Content-type: text/html; charset=utf-8");
my $body;
my $file;
my $kanaflg=0;
my $updatetitle;
if($nojapaneseflg) {
	$file=$english_file;
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
			s/\@\@ENGLISHIMAGE\@\@/@{[$mobileflg ? '' : '<div style="text-align:center;" align="center"><img src="title_eng.jpg" width="300" \/><\/div>']}/;
			s/\@\@VER\@\@/$VER/;
			s/\@\@INCLUDE\=\"(.+)\"\@\@/@{[&include($1)]}/;
			s/\@\@QRCODE\@\@/@{[&qrcode_link]}/;
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
	if(&load_module("GD::Barcode")) {
		return <<FIN;
携帯へURLを送るには、こちらのQRコードをご利用下さい。<br />
<img alt="QRCode" src="$basehost$basepath/area.cgi?m=qr\&amp;str=$string" />
FIN
	}
	'';
}
