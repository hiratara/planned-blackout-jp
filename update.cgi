#!/usr/bin/perl
use strict;
use warnings;

use CGI;
use LWP::Simple;
use FindBin;
use Archive::Tar;

# http://bizoole.com/power/のファイル更新 スクリプト
# update.cgiを実行することで、tgzを取得し、同階層のファイルを入れ替えます
# 作成 @iRSS http://d.hatena.ne.jp/iRSS/20110317/1300328160
#tarファイル取得
my $cgi = CGI->new;
my $file = $cgi->param('file') || 'power110316.tgz';
my $force = $cgi->param('force') || 0;

my $file_path = "$FindBin::RealBin/$file";
my $url = "http://bizoole.com/power/$file";


print $cgi->header(-type => 'text/plain',-charset => 'UTF-8');

if ($force && -f $file_path){
    unlink $file_path;

}

my $status = mirror($url,$file_path);
if (is_error($status)) {
    print "status:$status\t$urlの取得に失敗しました\n";
    exit
}else{
    if ($status == 304){
        print "status:$status\t$url 更新無し\n";
        exit;
    }else{
        print "status:$status\t$urlダウンロード成功\n";
    }
}

my $tar = Archive::Tar->new($file_path); 
my @files = $tar->list_files();
$tar->setcwd( $FindBin::RealBin);
print "$file_path 解凍\n";
$tar->extract();
my $tar_dir;
for (@files){
    my ($dir,$item) = split("/",$_);
    if ($item && -f "$FindBin::RealBin/$dir/$item"){
        my $cmd = "mv $FindBin::RealBin/$dir/$item $FindBin::RealBin/";
        print $cmd ."\n";
        `$cmd`;
    }else{
        $tar_dir = $dir;
    }
}
rmdir $tar_dir or die $!;

print "更新完了  \n";

