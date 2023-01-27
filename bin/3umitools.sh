#!/usr/bin/bash
#SBATCH --mem 15000
umi_tools dedup --stdin=$1  > $2
#umi_tools dedup --stdin=sortedcatpkp2mod.bam > dedupcatpkp2mod.bam
