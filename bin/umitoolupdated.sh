#!/usr/bin/bash
#SBATCH --mem 5000

umi_tools extract -p NNNNNNNNNNNN -I $1 --read2-in=$2  -S $3 --read2-out=$4  
