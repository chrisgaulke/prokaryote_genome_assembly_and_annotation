#!/bin/bash
INCREMENTS=2
MIN_VALUE=51
MAX_VALUE=199

OUTPUT_LOG="./autoResults.txt"
OUTPUT_NODES="./bestNodes.txt"
OUTPUT_N50="./bestN50.txt"
FIELD1=5
FIELD2=10


if [ $# -lt 2 ];
then
	echo "Incorrect arguemnts. Please provide an R1 and R2 file location"
	exit 1
fi

VELVET_BASE="assem"
VELVET_R1=$1
VELVET_R2=$2

rm -f $OUTPUT_LOG
rm -f $OUTPUT_NODES
rm -f $OUTPUT_N50



for kmer in `seq $MIN_VALUE $INCREMENTS $MAX_VALUE`;
do
	
	#VELVETH RUN
	velveth $VELVET_BASE$kmer $kmer -shortPaired -separate -fastq $VELVET_R1 $VELVET_R2 
	#VELVETG RUN
	velvetgCMD="velvetg $VELVET_BASE$kmer -read_trkg yes -exp_cov auto -cov_cutoff auto -min_contig_lgth 250"
	outputLine=$( $velvetgCMD | grep "Final graph")

	#RM the output file of velvet
	rm -rf $VELVET_BASE$kmer

	echo "$kmer: $outputLine" >> $OUTPUT_LOG

done

bestNodes="$(sort -n -k $FIELD1 $OUTPUT_LOG | head -n 3)"
bestN50="$(sort -n -r -k $FIELD2 $OUTPUT_LOG | head -n 3)"

echo "$bestNodes" > $OUTPUT_NODES
echo "$bestN50" > $OUTPUT_N50

topNode="$(cat $OUTPUT_NODES | head -n 1)"
topN50="$(cat $OUTPUT_N50 | head -n 1)"

if [[ $topNode == $topN50 ]];
then
	echo Top N50 and Top Nodes matched. Generating report...
	kmer=$(echo $topNode | cut -d ':' -f 1)
	#VELVETH RUN
	velveth $VELVET_BASE$kmer $kmer -shortPaired -separate -fastq $VELVET_R1 $VELVET_R2 
	#VELVETG RUN
	velvetg $VELVET_BASE$kmer -read_trkg yes -exp_cov auto -cov_cutoff auto -min_contig_lgth 250
else
	echo They did not match. Please inspect the log files.
fi




