#!/usr/bin/bash
#SBATCH --mem 5000
#samtools fastq dedupcatpkp2mod.bam > mergededupcatpkp2mod.fastq
samtools fastq $1 > $2
