#!/usr/bin/python

# TODO(karl): Add support for numerical ranges if necessary.

import argparse
import random
import sys

def main():
    args = parse_args()
    
    if args.num_rows is not None:
        result = sample_random(args.num_rows, args.input_file)
    elif args.rows is not None:
        result = get_rows(args.rows, args.input_file)
    else:
        sys.exit("Either --num_rows or --rows must be provided.")

    with open(args.output_file, "w") as output_file:
        output_file.write(result)

def parse_args():
    parser = argparse.ArgumentParser(description="Gets a subset of rows of a "
                                     "given file.")
    parser.add_argument("-n", "--num_rows", dest="num_rows", type=int,
                        help="The number of rows we want to randomly "
                        "sample from the csv file.")
    parser.add_argument("-r", "--rows", dest="rows", 
                        help="A comma seperated list of row numbers we would "
                        "like to get from the file.")
    parser.add_argument("-i", "--input_file", dest="input_file",
                        help="The input file.", required=True)
    parser.add_argument("-o", "--output_file", dest="output_file",
                        help="The output file.", required=True)
    return parser.parse_args()

def sample_random(num_rows, input_file):
    random.seed()
    input_len = file_len(input_file)
    if input_len < num_rows:
        print "Warning: num_rows is greater than the actual number of rows."
        num_rows = input_len
    # Could probably optimize this by using a set instead of fisher yates.
    possible_rows = [str(i) for i in xrange(0, input_len)]    

    # Do a partial fisher-yates shuffle
    for i in xrange(0, num_rows):
        num = random.randint(i, input_len)
        temp = possible_rows[num]
        possible_rows[num] = possible_rows[i]
        possible_rows[i] = temp
    print "Ok getting ", possible_rows[0:num_rows]
    return get_rows(",".join(possible_rows[0:num_rows]), input_file)

def get_rows(rows, input_file):
    rows = rows.split(",")
    rows = map(int, rows)
    rows.sort()
    results = []
    with open(input_file) as f:
        for i, line in enumerate(f):
            if not rows:
                break
            if i == rows[0]:
                results.append(line)
                rows.pop(0)

    return "".join(results)

def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == "__main__":
    main()
