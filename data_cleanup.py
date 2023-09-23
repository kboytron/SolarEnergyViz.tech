import csv

# Specify the path to your input and output CSV files
input_csv_file = 'C:/Users/Sai Tarun/PycharmProjects/Hackathon/solar_data.csv'
output_csv_file = 'C:/Users/Sai Tarun/PycharmProjects/Hackathon/clean_solar_data.csv'

# Function to check if a string can be converted to a number (float)
def is_numeric(s):
    try:
        # Attempt to convert the value to a float
        float(s)
        return True
    except ValueError:
        return False

# Read the input CSV file and clean the data
with open(input_csv_file, 'r', newline='') as infile, open(output_csv_file, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    for row in csv_reader:
        # Check if all values in the row (except for date columns) are numeric
        if is_numeric(row[4]):
            # Write the row to the output CSV file
            csv_writer.writerow(row)

print("CSV cleanup complete. Cleaned data saved to", output_csv_file)
