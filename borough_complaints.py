import argparse #Read -i, -s, -e, and -o from the terminal
import csv #Read and write CSV files correctly
import sys #Send output to the terminal using sys.stdout
from datetime import datetime #Convert dates from strings into values we can compare

"""
Count complaint types by borough within a given date range.

Outputs to an output file if provided, otherwise to stdout.

"""

def parse_arguments():
# parser that will parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
# add_argument() tells the parser to recognize an argument.
# "-i" is the short version of the argument.
# "--input" is the longer version. Both work!
# required=True means the user must provide an input filename.
# help="..." explains the argument when someone runs -h.

    parser.add_argument("-s", "--start", required=True, help="Start date")
    parser.add_argument("-e", "--end", required=True, help="End date")
    parser.add_argument("-o", "--output", required=False, help="Output CSV file")

#creating this way removes need for position => user can put them in any position and the -i, -s, -e, -o help the program know where they belong!

    return parser.parse_args() #read arguments and returns them


def count_complaints(filename, start, end):
    counts = {} #create an empty dictionary

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file) #lets us read each row as a dictionary, using the CSV column names as keys.

        for row in reader: #go through each row (each complaint) => each row is a dictionary
            created = datetime.strptime(
                row["Created Date"], "%m/%d/%Y %I:%M:%S %p" #dictionary_name[key] gives you value of that key
            ).date()

            if created < start or created > end: 
                continue

            complaint = row["Complaint Type"]
            borough = row["Borough"]

            key = (complaint, borough)

            if key not in counts:
                counts[key] = 0

            counts[key] += 1

    return counts


def write_results(counts, output_filename):
    if output_filename:
        output = open(output_filename, "w", newline="")
    else:
        output = sys.stdout

    writer = csv.writer(output)
    writer.writerow(["complaint type", "borough", "count"])

    for (complaint, borough), count in sorted(counts.items()):
        writer.writerow([complaint, borough, count])

    if output_filename:
        output.close()


def main():
    args = parse_arguments() #read arguments and store them

#dates are originally sring -> convert them to numbers
    start = datetime.strptime(args.start, "%m/%d/%Y").date()
    end = datetime.strptime(args.end, "%m/%d/%Y").date()

    counts = count_complaints(args.input, start, end)

    write_results(counts, args.output)


if __name__ == "__main__":
    main()
  
