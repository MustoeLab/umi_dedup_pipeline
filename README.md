Pipeline for deduplicating paired .fastq files which contain a UMI via the umicollapse package.

Run python dedup.py -h a list of all arguments.

Note - To reproduce ShapeMapper results prior to header correction patch, please run with --disable_header_correction (Necessary to reproduce results from msDMS-MaP paper)

##################
##################
Usage instructions
##################
##################

1. Activate the umi environment:
"conda activate umi_env"

2. bowtie2 index the fasta file in place:
"bowtie2-build -f gene.fa gene"

3. Run the deduplication pipeline:
"python /storage/mustoe/software/umi_dedup_pipeline/dedup.py --R1 r1.fastq --R2 r2.fastq --fasta gene.fa"

Additional notes:
There are also options for naming output files, changing the expected umi length, keeping temp files, changing number of processors bowtie2 is aligning with, and even an option to automatically index the fasta in place. These may all be seen by running dedup.py.

Step 2 of this process may be skipped by adding "--index_fasta" flag to the dedup.py arguments.

If you every get the error "Please ensure that all dependencies are installed" it likely means you forgot to switch to umi_env.

###########################
Reinstallation Instructions
###########################
To reconfigure umi dedup pipeline from source you must create a new conda environment housing dependencies, Download / modify UMICollapse, and place umicollapse in your absolute path

1. Create a new conda environment
"conda env create -f umi_env.yml"

This will create a new conda environment named umi_env with necessary dependencies installed.

2. Download umi collapse from https://github.com/Daniel-Liu-c0deb0t/UMICollapse
"git clone https://github.com/Daniel-Liu-c0deb0t/UMICollapse.git"

Navigate to the UMICollapse directory and modify the "umicollapse" file from
Java -server -Xms8G -Xmx8G -Xss20M -jar umicollapse.jar $@
to
Java -server -Xms8G -Xmx8G -Xss20M -jar /absolute/path/to/UMICollapse/umicollapse.jar $@

3. Add UMICollapse to the path variable in your bashrc / whatever config file you use on your system

Dependencies:
umitools, bowtie2, samtools, UMICollapse, Java11
