#!/usr/bin/bash
#SBATCH --mem 10000
samtools view -S -b $1 > $2
#samtools view -S -b catpkp2mod.sam > catpkp2mod.bam

