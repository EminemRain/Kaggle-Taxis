import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Gets a numbered data point from each line")
    parser.add_argument("-d", "--data_point", dest="data_point", type=int,
                        help="The data point we wamt from each line")
    parser.add_argument("-r", "--rows", dest="rows", 
                        help="A comma seperated list of row numbers we would "
                        "like to get from the file.")
    parser.add_argument("-i", "--input_file", dest="input_file",
                        help="The input file.", required=True)
    parser.add_argument("-o", "--output_file", dest="output_file",
                        help="The output file.", required=True)
    return parser.parse_args()

# Get args
args = parse_args()

# Get file name from command line and open the file
f = open(args.input_file, 'r')

# Iterate through, grab chosen data points from each line 
dataPointNum = args.data_point
outputData = []
for line in f:
    data = line.split(",")

    if args.data_point is not None:
        if dataPointNum < 9: 
            dataPoint = data[dataPointNum].replace("\"", "")
            outputData.append(dataPoint + "\n")
        else:
            outputData.append(data[dataPointNum:len(data)])
    elif args.rows is not None:
        rows = args.rows
        rows = rows.split(",")
        rows = map(int, rows)
        rows.sort()
        length = len(rows)
        for r in rows:
            length -= 1
            dataPoint = data[r].replace("\"","")
            if length == 0:
                outputData.append(dataPoint + "\n")
            else:
                outputData.append(dataPoint + ",")
	

results = "".join(outputData)
with open(args.output_file, "w") as output_file:
        output_file.write(results)



