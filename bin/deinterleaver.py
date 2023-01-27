import sys

with open(sys.argv[1], 'r') as deinterleave:
   with open(sys.argv[2], 'w') as R1:
      with open(sys.argv[3], 'w') as R2:
        lines = deinterleave.readlines()
        lines.insert(0, "")
        R1lines = []
        R2lines = []

        flag = 1
        for i in range(1, len(lines)):
           #print(i)
           if(flag == 1):
            # print("flag = 1") 
             R1lines.append(lines[i]) 
             if(i % 4 == 0):
               flag = 2
           else:
             #print("flag = 2")
             R2lines.append(lines[i]) 
             if(i % 4 == 0):
               flag = 1


        for line in R1lines:
           R1.write(line)

        for line in R2lines:
           R2.write(line)

        #print("R1 lines")
        #print(R1lines)
        #print("R2 lines")
        #print(R2lines)
