import sys

# Such simple logic, avoiding argparse
i_file = sys.argv[1]
o_file = sys.argv[2]

# Strip /1 and /2 from end of header of reads since it interferes
# With Bowtie2 alignment
with open(i_file, "r") as o_i_file, open(o_file, "w") as o_o_file:

    read = []
    for line in o_i_file:
        read.append(line)

        if len(read) == 4:
            read[0] = read[0].replace("/2", "").replace("/1", "") 
            o_o_file.writelines(read)
            read = []
