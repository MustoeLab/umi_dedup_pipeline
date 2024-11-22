Pipeline for deduplicating paired .fastq files which contain a UMI.

Run python dedup.py -h for usage instruction.

Note - To reproduce ShapeMapper results prior to header correction patch, please run with --disable_header_correction (Necessary to reproduce results from msDMS-MaP paper)

Dependencies:
umitools, bowtie2, samtools, UMICollapse, Java11
