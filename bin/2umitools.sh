#!/usr/bin/bash
#SBATCH --mem 5000
umi_tools group -I $1 --group-out=$2 --output-bam -S $3
#umi_tools group -I sortedcatpkp2mod.bam --group-out=umigroupscatpkp2mod.tsv --output-bam -S sorted_grouped_catpkp2mod.bam
