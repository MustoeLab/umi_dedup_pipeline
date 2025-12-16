import sys
fastq = sys.argv[1]
R2 = sys.argv[2]
if R2 == "False":
    R2 = False
else:
    R2 = True

with open(fastq, "r") as o_file:
    umis = set()
    line_num = 0
    for line in o_file:
        if ( line_num % 4 ) == 0: # Then this is the header
           umi = line.rstrip().split("_")[-1]
           umis.add(umi)

        line_num += 1

#    print(f"Total number of umis: {len(umis)} across {int(len(lines) / 4)} lines")
    if R2:
        reads = int(line_num / 8)
    else:
        reads = int(line_num / 4)
    print(f"Total number of umis: {len(umis)} across {reads} reads in the aligned SAM file")
