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
# 2011/03/18 修正 tarボールファイル名を'power_latest.tgz'に変更
#
#
#tarファイル取得
my $cgi = CGI->new;
my $file = $cgi->param('file') || 'power_latest.tgz';
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
}else{
    if ($status == 304){
        print "status:$status\t$url 更新無し\n";
    }else{
        print "status:$status\t$urlダウンロード成功\n";
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
    }
}


# all.all runtable.txt timetable.txtの更新
# コード冗長すぎてはずかし。
my @files = qw(all.all runtable.txt timetable.txt);
for my $file (@files){
    my $file_path = "$FindBin::RealBin/$file";
    my $url = "http://bizoole.com/power/$file";
    if ($force && -f $file_path){
        unlink $file_path;
    }
    my $status = mirror($url,$file_path);
    if (is_error($status)) {
        print "status:$status\t$urlの取得に失敗しました\n";
    }else{
        if ($status == 304){
            print "status:$status\t$url 更新無し\n";
        }else{
            print "status:$status\t$urlダウンロード成功\n";
        }
    }
}

print "完了  \n";

