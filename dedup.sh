#!/usr/bin/bash
#SBATCH -n 8
#SBATCH --mem=10000

################################
################################
# Lucas Kearns / Thomas Miller
# 25 Oct 2022
# Mustoe Lab - Baylor College of Medicine
# UMI Deduplication Pipeline
################################
################################



#Usage Notes:
#Must index fasta file and place output of index in same
#folder as dedup.sh or in the path specified in optional 4th argument.
#IE bowtie2-build -f FILE.fa FILE

#Must input read one and two of a fastq file as well as
#the corresponding fasta file.
#However, do not included the .fa on the gene name

#Must change the set of Ns within  umitool.sh to correspond with UMI format, 
#Currently set to 12 consecutive N. Additionally, this assumes the UMI is on the 5’ end of read1 starting from NT 1. If the UMI is elsewhere this will need to be changed.

#Can name output files by formatting the optional path to run location as path/prefix

#Be sure to include the / at the end of the path to the run location so this is formatted
#correctly within the code IE /storage/mustoe/home/ not /storage/mustoe/home 

#Note to rename output reads, you must include a path to the run location

#Additionally, if you want to run multiple instances of deduplication
#from within the same folder you must rename the output reads so the temp
#files do not overlap.
dir=${BASH_SOURCE}
path=$( dirname $BASH_SOURCE; )
binpath="${path}/bin/"
if [ $# -eq 0 ]
then
	echo "USAGE: r1.fastq  r2.fastq  gene  {Optional:Path to run location} {Optional:Name of output}"
   echo $path
   echo $binpath
else

prefix=""
inp1=$1
inp2=$2
inp3=$3

name="${inp3}dedup"
nameset=false

if [ $# -gt 3 ]
then
   prefix=$4
   if [ $# -eq 5 ]
   then
      name=$5
      nameset=true
fi
fi


bowtie_sam="${prefix}sample.sam"
bowtie_bam="${prefix}sample.bam"
bowtie_bam2="${prefix}sortedsample.bam"
dedup="${prefix}sortedsamplededup.bam"
dedup_by_name="${prefix}sortedsamplebynamededup.bam"
final_out="${prefix}${inp3}dedup.fastq"
read1umi="${prefix}umi${inp1}"
read2umi="${prefix}umi${inp2}"
interleaved_fastq="${prefix}interleaved_fastq.fq"
final_out_1="${prefix}${name}_R1.fastq"
final_out_2="${prefix}${name}_R2.fastq"

if [ nameset ]
then
   bowtie_sam="${prefix}${name}sample.sam"
   bowtie_bam="${prefix}${name}sample.bam"
   bowtie_bam2="${prefix}${name}sortedsample.bam"
   dedup="${prefix}${name}sortedsamplededup.bam"
   dedup_by_name="${prefix}${name}sortedsamplebynamededup.bam"
   final_out="${prefix}${name}${inp3}dedup.fastq"
   read1umi="${prefix}${name}umi${inp1}"
   read2umi="${prefix}${name}umi${inp2}"
   interleaved_fastq="${prefix}${name}interleaved_fastq.fq"
   final_out_1="${prefix}${name}_R1.fastq"
   final_out_2="${prefix}${name}_R2.fastq"
fi


if [ $# -gt 3 ]
then
   inp1=$prefix$1
   inp2=$prefix$2
   inp3=$prefix$3
fi
#Extracts UMIs
${binpath}umitoolupdated.sh $inp1 $inp2 $read1umi $read2umi
echo "Updated umitool completed"
#aligns the reads
echo "bowtie2updated.sh $inp3 $read1umi $read2umi $bowtie_sam"
${binpath}bowtie2updated.sh $inp3 $read1umi $read2umi $bowtie_sam
echo "bowtie completed"
#Converts from sam into binary
${binpath}samtools.sh $bowtie_sam $bowtie_bam
echo "Samtools completed"
#sorts bam file
${binpath}2samtools.sh $bowtie_bam $bowtie_bam2
echo "2samtools completed"
#indexes bam file
${binpath}3samtools.sh $bowtie_bam2
echo "3samtools completed"
#Deduplicates umis
umicollapse bam -p .05 -i $bowtie_bam2 -o $dedup --paired
echo "Umicollapse completed"
#Sorts by name
${binpath}5samtools.sh $dedup $dedup_by_name
echo "Sorted bam file by name"
#Converts from bam into fastq
${binpath}4samtools.sh $dedup_by_name $final_out
echo "Converted from bam to fastq"
#Deinterleaves the fastq file into separate R1 and R2 files
python ${binpath}deinterleaver.py $final_out $final_out_1   $final_out_2
echo "Interleaved file de interleaved and deduplicated reads 1 and 2 produced"


rm ${bowtie_sam}
rm ${bowtie_bam}
rm ${bowtie_bam2}
rm ${dedup}
rm ${dedup_by_name}
rm ${final_out}
rm ${read1umi}
rm ${read2umi}
rm "${bowtie_bam2}.bai"
echo "cleaned up intermediate files"






fi
