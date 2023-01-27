#!/usr/bin/bash
#SBATCH --mem 10000

#samtools sort $1 -o $2
samtools sort $1 -o $2 -n
#samtools sort catpkp2mod.bam -o sortedcatpkp2mod.bam

