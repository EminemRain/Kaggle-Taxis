#!/usr/bin/python

# TODO(karl): Add support for numerical ranges if necessary.

import argparse
import random
import sys
import utils
import string

def main():
    args = parse_args()
    
    (result_test, result_answer) = transform_rows(args.input_file)

    with open(args.output_file_prefix + "_" + "test.csv", "w") as output_file:
        output_file.write(result_test)
    with open(args.output_file_prefix + "_" + "answer.csv", "w") as output_file:
        output_file.write(result_answer)

def parse_args():
    parser = argparse.ArgumentParser(description="Gets a subset of rows of a "
                                     "given file.")
    parser.add_argument("-i", "--input_file", dest="input_file",
                        help="The input file.", required=True)
    parser.add_argument("-o", "--output_file_prefix", dest="output_file_prefix",
                        help="The prefix for the answer and test files.",
                        required=True)
    return parser.parse_args()

def transform_rows(input_file):
    random.seed()
    input_results = []
    output_results = []
    with open(input_file) as f:
        for line in f:
            path = utils.get_column(utils.Columns.path, line)
            if len(path) == 0:
                continue
            end = random.randint(0, len(path))
            input_row = ",".join(string.split(line, ",", 8)[:8]) + ","
            input_row += utils.path_to_csv(path[:end])
            input_results.append(input_row)
            output_row = "\"T" + str(utils.get_column(utils.Columns.trip_id, line)) + "\""
            output_row += "," + str(path[-1][0]) + "," + str(path[-1][1])
            output_results.append(output_row)
    return ("\n".join(input_results), "\n".join(output_results))

if __name__ == "__main__":
    main()
