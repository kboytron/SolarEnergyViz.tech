import pandas as pd

# Load the dataset
data = pd.read_csv('data/hourly_energy_conversion.csv')

# Convert the dataset to JSON
data_json = data.to_json(orient='records')

# Write the JSON data to a file
with open('html/hourly_energy_conversion.json', 'w') as outfile:
    outfile.write(data_json)
