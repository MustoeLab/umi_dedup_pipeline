#!/usr/bin/bash
#SBATCH --mem 2000

/storage/mustoe/home/u246626/software/BBTools/bbmap/bbmerge.sh in1=$1 in2=$2 out=$3 outu=$4 ihist=$5
