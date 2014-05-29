#!/usr/bin/perl

if(@ARGV < 6){
	die "Usage: $0 <question strings> <q parses> <p strings> <p parses> <n strings> <n parses> (<length constraint>)\n";
}

if(@ARGV == 7){
	$maxlen = $ARGV[6];
}else{
	$maxlen = 999999999;
}

open(QSTR, $ARGV[0]);
open(QPAR, $ARGV[1]);
open(PSTR, $ARGV[2]);
open(PPAR, $ARGV[3]);
open(NSTR, $ARGV[4]);
open(NPAR, $ARGV[5]);

$item = 1;

while($qstr = <QSTR>){
	if($qstr =~ m/<[A-Z]\s+(\d+\.?\d*)\s+>/){
		$label = $1;
		processQuestion();
	}
}

sub processQuestion{
	print "<QApairs id='$label'>\n";
	print "<question>\n";

	for($i=0; $i<5; $i++){
		$qpar = <QPAR>;
		print $qpar;
	}
	<QPAR>;

	print "</question>\n";
	processPositives();
	processNegatives();	

	print "</QApairs>\n";
}

sub processPositives(){
	<PSTR>;
	while($str = <PSTR>){
		chomp($str);
		if($str =~ /^<\/A>$/){
			last;
		}
		$res = "<positive>\n";
		for($i=0; $i<5; $i++){
			$par = <PPAR>;
			@parts = split(/\t+/, $par);
			if(@parts > $maxlen){
				$res = "";
				<PPAR>; <PPAR>; <PPAR>; <PPAR>;
				last;
			}
			$res .= $par;
		}
		<PPAR>;

		if($res ne ""){
			$res .= "</positive>\n";
			print $res;
		}
	}
}

sub processNegatives(){
	<NSTR>;
	while($str = <NSTR>){
		chomp($str);
		if($str =~ /^<\/A>$/){
			last;
		}
		$res = "<negative>\n";
		for($i=0; $i<5; $i++){
			$par = <NPAR>;
			@parts = split(/\t+/, $par);
			if(@parts > $maxlen){
				$res = "";
				<NPAR>; <NPAR>; <NPAR>; <NPAR>;
				last;
			}
			$res .= $par;
		}
		<NPAR>;

		if($res ne ""){
			$res .= "</negative>\n";
			print $res;
		}
	}
}
