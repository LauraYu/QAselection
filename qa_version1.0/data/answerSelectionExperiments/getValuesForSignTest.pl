#!/usr/bin/perl

#pass in two (paired) lists of numbers

#to perform a sign test, compute the probability of seeing at least $numgreater positive events
#when drawing ($numless+$numgreater) samples from a binomial distribution with parameter 0.5.
#
#i.e., the p-value is the probability of ($numless+$numgreater) coin flips turning up heads at least $numgreater times.


if(@ARGV != 2){
	die "pass in two lists of paired numbers.\n";
}

open(IN1, $ARGV[0]);
open(IN2, $ARGV[1]);
while($line1 = <IN1>){ 
	$line2 = <IN2>; 
	chomp $line1; 
	chomp $line2; 
	print STDERR "$line1\t$line2\n";

	if($line1 > $line2){
		$numgreater++;
	}
	if($line1 < $line2){
		$numless++;
	}
	$total++;
}

print "total:$total\n";
print "numGreater:\t$numgreater\n";
print "numLess:\t$numless\n";
print "effectiveSampleSize:\t".($numless+$numgreater)."\n";


