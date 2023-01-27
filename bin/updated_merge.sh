#!/usr/bin/bash
#SBATCH --mem 2000
#SBATCH -n 4

/storage/mustoe/home/u246626/software/BBTools/bbmap/bbmerge.sh vstrict=t interleaved=t usejni=t t=4 in=$1 out=$2 outu=$3 ihist=$4

