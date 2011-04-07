#!/usr/bin/perl

use strict;

my $VER="V.1.143(nanakochi123456  1st release:mnakajim)";
my $tarball="power110328.tar.gz";
my $history=<<EOM;
<h3>データ更新状況:</h3>
<ul id="update">
<li>2011/3/28 06:06 twitter情報が完全でなかった為、ホームページより入手した情報を入力した。</li>
<li>2011/3/27 22:07 東京電力のデータを更新した。またtwitter情報によりグループ２の詳細を入力した。</li>
<li>2011/3/27 12:54 東北電力のデータを更新した。なお省略部分がある為、市町村までの入力で一度検索してみて下さい。</li>
<li>2011/3/27 20:11 東京電力側のデータに欠損があった為、反映した。</li>
<li>2011/3/27 13:17 本家に対応しやすいように、all.allを変更した。</li>
<li>2011/3/26 09:17 東京電力3月26日更新データに更新した。東京都にもサブグループが付くようになります。</li>
<li>2011/3/26 03:16 東京電力２５グループ化に対応した。なお、東京都は現状ではデータがない為、今まで通りの表示となります。</li>
<li>2011/3/25 18:40 東京電力２６日、２７日実施なしに対応した。</li>
<li>2011/3/25 03:14 東京電力データを更新した。</li>
<li>2011/3/24 18:43 25日の１，３，４，５グループの計画停電なしに対応した。</li>
<li>2011/3/24 12:00 英語版のローマ字振りの一部が変換されていなかったのを修正した。</li>
<li>2011/3/24 06:06 東京電力の第２、第３、第４グループの実施なしに対応した。また東北電力も実施なしです。</li>
<li>2011/3/24 00:40 東京電力のデータを更新した。一番最後の終了時刻が22:10になっていたのを修正した。</li>
<li>2011/3/23 14:30 ローマ字データが一部変換をミスっていたのを修正した。</li>
<li>2011/3/23 05:55 東京電力のデータを更新した。</li>
<li>2011/3/22 10:30 東京電力のデータを更新した。これにより茨城県がしばらく計画停電の範囲外になる模様です。</li>
</ul>
<a href="http://power.daiba.cx/wiki/?%a5%c7%a1%bc%a5%bf%b9%b9%bf%b7%cd%fa%ce%f2">これ以前の当方のデータ更新履歴</a><br />
<a href="http://bizoole.com/power/history/datahistory.html">これ以前の本家のデータ更新履歴</a>

<h3>エンジン更新履歴:</h3>
<ul id="engine">
<li>2011/3/27 12:54 ローマ字でスペースが入っていると検索できないバグを直した。</li>
<li>2011/3/27 07:30 area.cgi?comm=ver の返り値を本家とほぼ同じにした。文字正規化方法を本家と同じにした。携帯版での色出力を抑制した(パケ代節約のため)</li>
<li>2011/3/25 13:16 本家に対応しやすいように、エンジンを変更した。</li>
<li>2011/3/25 18:40 東京電力のグループが 1-Aや、5-Cになるのを仮対応した。</li>
<li>2011/3/24 09:44 カタカナ、及びローマ字で検索できるようにした。</li>
<li>2011/3/24 08:28 index.cgi を書き換えた。そのため、出力ファイル3ファイルが追加されます。</li>
<li>2011/3/24 13:32 バージョン (または 試験、更新、update、ver）を検索文字列に入れると、エンジンのバージョン及びデータベース等のタイムスタンプを出力するようにした。</li>
<li>2011/3/24 12:00 全スクリプトを use strict; にした。</li>
<li>2011/3/24 10:20 TOPページにも可能であればQRコードを表示できるようにした。また、一部ファイルを分割した。</li>
<li>2011/3/24 06:40 地域名入力と郵便番号入力フォームを統合した。なお、携帯版のみ入力の簡易化の為に残してあります。</li>
<li>2011/3/24 00:40 TOPページにおいて携帯から英語ページに行こうとしても、英語ページにいけなくなったのを修正した。</li>
<li>2011/3/23 17:23 検索結果のQRコードを出力できるようにした。GD::Barcodeモジュールがない場合は出力されません。</li>
<li>2011/3/23 13:26 エンジン最新にして、軽量化を図った。RSSで郵便番号で検索した場合、一部バグるのを修正した。</li>
<li>2011/3/22 19:00 23日の東京電力の1回目の１、２グループにおいて実施しないことを反映した。</li>
<li>2011/3/22 17:30 英語版にて、１文字目大文字、それ以上の文字を小文字にしました。また、area.cgiにおいてもgzip圧縮をしました。</li>
<li>2011/3/22 16:00 英語版（β）を作成した。なお、地名変換には、Kakasiを使用しています。</li>
<li>2011/3/22 11:40 22日東京電力　第１及び５グループ２回目計画停電なしに対応。</li>
<li>2011/3/22 10:30 事前にall.allを最適化しておくことで、検索時間をわずかに最適化した。</li>
</ul>
<br />
<a href="http://power.daiba.cx/wiki/?%a5%a8%a5%f3%a5%b8%a5%f3%b9%b9%bf%b7%cd%fa%ce%f2">これ以前の当方のエンジン更新履歴</a><br />
<a href="http://bizoole.com/power/history/">これ以前のエンジン更新履歴</a>
EOM

#------------
require "common.pl";

$VER=~s/\(.*//g;
my $nojapaneseflg=0;
$nojapaneseflg=1 if($ENV{HTTP_ACCEPT_LANGUAGE}!~/ja/);
my $mobileflg=0;
$mobileflg=1 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/);

$mobileflg=0 if($ENV{QUERY_STRING} eq 'p');
$mobileflg=1 if($ENV{QUERY_STRING} eq 'm');
$nojapaneseflg=0 if($ENV{QUERY_STRING} eq 'p');
$nojapaneseflg=1 if($ENV{QUERY_STRING} eq 'e');

my $english_file="english.html";
my $mobile_file="mobile.html";
my $pc_file="pc.html";

&gzip_compress("Content-type: text/html; charset=utf-8");
my $body;
my $file;
if($nojapaneseflg) {
	$file=$english_file;
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
			s/\@\@QRCODE\@\@/@{[&qrcode_link]}/;
			s/\@\@HISTORY\@\@/$history/;
			s/\@\@TARBALL\@\@/$tarball/;
		}
		$body.=$_;
	}
	close(R);
} else {
	$body="$file not found. sorry.";
}

print "$body\n";

#close(STDOUT);
exit;

sub include {
	my $file=shift;
	my $body;
	if(open(I,$file)) {
		foreach(<I>) {
			$body.=$_;
		}
		close(I);
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
