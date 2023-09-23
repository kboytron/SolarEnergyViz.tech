import csv

Silliken_size = 16.7225
if __name__ == '__main__':
    path = "C:/Users/Sai Tarun/PycharmProjects/Hackathon/clean_solar_data.csv"
    daily_data = []
    hourly_data = []

    # Open the CSV file and read its contents
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Check if the row has at least 4 values (0-based indexing)
            if len(row) >= 4:
                # Store the 3rd and 4th values (0-based indexing) in a sub-array
                hourly_values = [row[3], row[4]]
                daily_values = [row[3], row[4]]

                # Append the sub-array to the data array
                daily_data.append(daily_values)
                hourly_data.append(hourly_values)

    #del daily_data[:2]

    for row in daily_data:

        print("Date: ",row[0],"  |  Daily kwh: ",row[1])
        daily_kwh = float(row[1])
        solar_irradiance = float(3)
        daily_conversion = daily_kwh/(solar_irradiance*Silliken_size)
        print("Daily conversion: ",daily_conversion,"\n")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
