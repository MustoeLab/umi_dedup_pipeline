import sys

with open(sys.argv[1], "r") as deinterleave, \
               open(sys.argv[2], "w") as R1, \
               open(sys.argv[3], "w") as R2:

    read = 0
    line_buffer = []
    for line in deinterleave:
        line_buffer.append(line)
        if len(line_buffer) == 4:
            read += 1
            if read % 2 != 0:
                R1.writelines(line_buffer)
            else:
                R2.writelines(line_buffer)

            line_buffer = []
