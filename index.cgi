#!/usr/bin/perl

use strict;

my $VER="V.1.145(nanakochi123456  1st release:mnakajim)";
my $tarball="power110328-5.tar.gz";
my $history=<<EOM;
<h3>データ更新状況:</h3>
<ul id="update">
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
</ul>
<a href="http://power.daiba.cx/wiki/?%a5%c7%a1%bc%a5%bf%b9%b9%bf%b7%cd%fa%ce%f2">これ以前の当方のデータ更新履歴</a><br />
<a href="http://bizoole.com/power/history/datahistory.html">これ以前の本家のデータ更新履歴</a>

<h3>エンジン更新履歴:</h3>
<ul id="engine">
<li>2011/3/28 20:34 バージョン情報へのリンクを追加した。また、バージョン情報の表示時にQRコード及びRSSのリンクを出力しないようにした</li>
<li>2011/3/28 08:04 東京電力が速報で一部サブグループのみの実施となった場合に、きちんと計画停電を実施するかしないかを明確にできるようにした。</li>
<li>2011/3/27 12:54 ローマ字でスペースが入っていると検索できないバグを直した。</li>
<li>2011/3/27 07:30 area.cgi?comm=ver の返り値を本家とほぼ同じにした。文字正規化方法を本家と同じにした。携帯版での色出力を抑制した(パケ代節約のため)</li>
<li>2011/3/25 13:16 本家に対応しやすいように、エンジンを変更した。</li>
<li>2011/3/25 18:40 東京電力のグループが 1-Aや、5-Cになるのを仮対応した。</li>
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
