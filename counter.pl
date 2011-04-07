use strict;
use Fcntl ':flock';

my $LOCK_SH=1;
my $LOCK_EX=2;
my $LOCK_NB=4;
my $LOCK_DELETE=128;
my $COUNTER_FILE="./counter/counter.txt";

sub counter_get {
	my %counter = &counter_do($COUNTER_FILE,"r");
	return <<"EOD";
Counter :  $counter{total}
StartDate : $counter{startdate}
EOD
}

sub counter_write {
	return &counter_do($COUNTER_FILE,"w");
}

sub counter_do {
	my %default;
	my($counter,$rw)=@_;
	my %counter;
	my %default;
	my $file = "$counter";
	my ($mday, $mon, $year) = (localtime)[3..5];
	$year += 1900;
	$mon += 1;
	$default{total}=0;
	$default{startdate}=sprintf('%04d-%02d-%02d',$year,$mon,$mday);

	my $counters=&lock_fetch($file);
	my $buf;
	if($counters!~/\d/) {
		$buf="$default{startdate}\n0\n";
		%counter=%default;
	} else {
		($counter{startdate},$counter{total})=split(/\n/,$counters);
		$counter{total}+=1 if($rw ne 'r');
		$buf="$counter{startdate}\n$counter{total}\n";
	}
	&lock_store($file,$buf);
	return %counter;
}

sub lock_store {
	my ($filename, $value) = @_;
	my $lfh;
	local $SIG{ALRM} = sub { die "time out" };

	eval {
		if(open(FILE, "+<$filename") or open(FILE, ">$filename")) {
			alarm(5);
			eval("flock(FILE, LOCK_EX)");
			if ($@) {
				$lfh=&lock($filename,$LOCK_EX);
				if(!$lfh) {
					alarm(0);
					return undef;
				}
			}
			alarm(5);
			truncate(FILE, 0);
			print FILE $value;
			alarm(5);
			eval("flock(FILE, LOCK_UN)");
			if ($@) {
				&unlock($lfh);
			}
			alarm(0);
			close(FILE);
		} else {
			alarm(0);
			return undef;
		}
		alarm(0);
	};
	if ($@ =~ /time out/) {
		return undef;
	}
	return $value;
}

sub lock_fetch {
	my ($filename) = @_;
	my $lfh;
	open(FILE, "$filename") or return(undef);
	eval("flock(FILE, LOCK_SH)");
	if ($@) {
		$lfh=&lock($filename,$LOCK_SH);
	}
	local $/;
	my $value = <FILE>;
	eval("flock(FILE, LOCK_UN)");
	if ($@) {
		&unlock($lfh);
	}
	close(FILE);
	return $value;
}

sub lock_delete {
	my ($filename) = @_;

	my $lfh;
	open(FILE, "$filename") or return(undef);
	eval("flock(FILE, LOCK_SH)");
	if ($@) {
		$lfh=&lock($filename,$LOCK_DELETE);
	}
	eval("flock(FILE, LOCK_UN)");
	close(FILE);
	unlink($filename);
}

sub lock {
	my $timeout=5;
	my $trytime=2;

	my($fname,$method)=@_;
	# ディレクトリ、ファイル名、拡張子を分離
	my($d,$f,$e)=$fname=~/(.*)\/(.+)\.(.+)$/;
	# ファイル名から記号らしきものを除去(短くするため)								$f=~s/[.%()[]:*,_]//g;
	# 初期ハンドルの作成
	my %lfh=(
		dir=>$d,
		basename=>$f,
		timeout=>$timeout,
		trytime=>($method & $trytime),
		fname=>$fname,
		method=>$method & 3,
		path=>"$d/$f.lk"
	);
	# ロックファイルの削除
	if($method eq $LOCK_DELETE) {
		return &lock_del(%lfh);
	}
	return if($lfh{method} eq 0);

	for(my $i=0; $i < $lfh{trytime}*10; $i++) {
		# ロックメソッド、プロセスID、現在時を入れる
		$lfh{current}=sprintf("%s/%s.%x.%x.%x.%d.lk"
			,$lfh{dir},$lfh{basename},$lfh{method},$$,time);
		# ロック、成功時は正常終了
		return \%lfh if(rename($lfh{path},$lfh{current}));

		# 過去のロックファイルを検索
		my @filelist=&lock_getdir(%lfh);
		my @locklist=();
		my $fcount=0;
		my $excount=0;
		my $shcount=0;
		foreach (@filelist) {
			if (/^$lfh{basename}\.(\d)\.(.+)\.(.+)\.lk$/) {
				push(@locklist,"$1\t$2\t$3");
				$fcount++;
				$shcount++ if($1 eq 1);
				$excount++ if($1 eq 2);
			}
		}
		# ロックファイルが存在しなければ新規作成
		if($fcount eq 0) {
			open(LFHF,">$lfh{path}");
			close(LFHF);
			next;
		# 共有ロックの場合
		} elsif($lfh{method} eq 1) {
			# 排他が存在しない場合
			if($shcount > 0 && $excount eq 0) {
				# １つチョイスして、リネームする
				foreach(@locklist) {
					my($method,$pid,$time)=split(/\t/,$_);
					my $orgf=sprintf("%s/%s.%x.%s.%s.lk"
						,$lfh{dir},$lfh{basename},$method,$pid,$time);
					# 再ロック
					return \%lfh if(rename($orgf,$lfh{current}));
				}
			}
		}
		# 排他であるor異常時
		# 0.1秒のsleep、使えなければ1秒
		eval("select undef, undef, undef, 0.1;");
		if($@) {
			sleep 1;
			$i+=9;
		}
	}
	# 再試行終了
	# 過去のロックファイルを検索
	my @filelist=&lock_getdir(%lfh);
	foreach (@filelist) {
		if (/^$lfh{basename}\.(\d)\.(.+)\.(.+)\.lk$/) {
			# タイムアウトしているのが存在したら
			if (time - hex($3) > $lfh{timeout}) {
				my $orgf=sprintf("%s/%s.%s.%s.%s.lk"
					,$lfh{dir},$lfh{basename},$1,$2,$3);
				return \%lfh if(rename($orgf,$lfh{current}));
			}
		}
	}
	return undef;
}

sub unlock {
	rename($_[0]->{current}, $_[0]->{path});
}

sub lock_del {
	my(%lfh)=@_;
	unlink($lfh{path});
	my @filelist=&lock_getdir(%lfh);
	foreach (@filelist) {
		if (/^$lfh{basename}\.(\d)\.(.+)\.(.+)\.lk$/) {
			unlink($_);
		}
	}
}

sub lock_getdir {
	my(%lfh)=@_;
	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);
	return @filelist;
}

