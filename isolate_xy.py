#This file was used to take only the variables to be used as x and y out of a
#.csv file and save them to a new file as two space-sepparated lines. The first
#line is x-values and the second is y-values.

#config variables
infile = "data/tempc12.txt"
outfile = "data/tempc12.txt"
x_key = 'DATE'
y_key = 'TEMPC'

file = open(infile, "r")

#find field index
#assumes x field comes first
x_index = -1
y_index = -1
line = file.readline().split(",")
for i in range(len(line)):
    if x_key in line[i]:
        x_index = i
    elif y_key in line[i]:
        y_index = i
        break
if x_index == -1 or y_index == -1:
    print("something wrong..")
    sys.exit()

#get that field from each line
x_data = []
y_data = []
for line in file:
    fields = line.split(",")
    x_data.append(fields[x_index])
    y_data.append(fields[y_index])
file.close()

#write data to outfile
file = open(outfile, "w")
for x in x_data:
    file.write(x+" ")
file.write("\n")
for y in y_data:
    file.write(y+" ")
file.close()
