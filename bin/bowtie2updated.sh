#!/usr/bin/bash
#SBATCH --mem 5000



#bowtie2 -x $1 -1 $2  -2 $3 -S $4
bowtie2 -p 8 --local --sensitive-local --mp 3,1 --rdg 5,1 --rfg 5,1 --dpad 30 --maxins 800 --ignore-quals --no-unal -x $1 -1 $2  -2 $3 -S $4 


