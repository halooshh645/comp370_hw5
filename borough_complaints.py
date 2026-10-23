import argparse
import csv # need this to be able to use DictReader()
from datetime import datetime # The first datetime is the module (a collection of tools for working with dates and times) and second datetime is a class inside that module that represents a date and time
import sys # need to write to standard ouput 

def count_complaints(input_file, start, end):

    count_dict = {} # This is dictionary we will use to keep track => keys will be tuples (Borough, Complaint) and Value will be number of this complaint in this Borough

    with open(input_file, 'r') as f:
        input_dicts = csv.DictReader(f) # Creates a dictionary for each row, with the first row(header) as key

        for input_dict in input_dicts:
            # Step 1: check if the creation date of this row falls into the creation date range provided as argument
            # Convert it to datetime object to be able to compare it:
            date_created = datetime.strptime(input_dict["Created Date"], "%m/%d/%Y %I:%M:%S %p").date()
            if start <= date_created <= end:
                # Step 2: check if the tuple key (borough, complaint) is already in count_dict => if yes, add 1 to value, if not, add it to count_dict
                if (input_dict["Borough"], input_dict["Complaint Type"]) in count_dict:
                    count_dict[input_dict["Borough"], input_dict["Complaint Type"]] += 1
                else:
                    count_dict[input_dict["Borough"], input_dict["Complaint Type"]] = 1

    return count_dict


def display(count_dict, output):
    
    if output != None:                           
        with open(output, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["complaint type", "borough", "count"])
            for (borough, complaint), count in count_dict.items():
                writer.writerow([complaint, borough, count])
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(["complaint type", "borough", "count"])
        for (borough, complaint), count in count_dict.items():
            writer.writerow([complaint, borough, count])
                                          

def most_common(count_dict):
    total = {}

    for (borough, complaint), count in count_dict.items():
        if complaint in total:
            total[complaint] += count
        else:
            total[complaint] = count

    most_common = max(total, key=total.get) # max(total) compares keys => adding key=total.get retrieves the values associated with keys and compares those
    return most_common, total[most_common]

def main():
    """

    Outputs number of each complaint type per borough for a given creation data range

    """
    parser = argparse.ArgumentParser() # creates a parser that understands command-line arguments
    
    parser.add_argument("-i", "--input", required=True, help="Path to input csv file") 
    parser.add_argument("-s", "--start", required=True, help="Creation range start date") 
    parser.add_argument("-e", "--end", required=True, help="Creation range end date")
    parser.add_argument("-o", "--output", required=False, help="Path to output csv file")

    args = parser.parse_args()    
    
    # Converting date arguments into datetime objects
    start = datetime.strptime(args.start, "%m/%d/%Y").date() #Here input is just date
    end = datetime.strptime(args.end, "%m/%d/%Y").date()

    count_dict = count_complaints(args.input, start, end)

    display(count_dict, args.output)




if __name__ == "__main__":
    main()

