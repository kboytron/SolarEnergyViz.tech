"""
Get DNI (solar radiance) for Iowa City for years 2011-2020 by hour

This data will be used to calculate Conversion Efficiency
Source: https://nsrdb.nrel.gov/data-viewer
"""

import pandas as pd
import urllib.parse
import os

API_KEY = "API-key"
EMAIL = "dtemi2@illinois.edu"
BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?"
POINTS = [
'814062'
]

def main():
    input_data = {
        'attributes': 'dni',
        'interval': '60',
        'to_utc': 'false',
        'half_hour': 'true',
        'include_leap_day': 'true',
        
        'api_key': API_KEY,
        'email': EMAIL,
    }
    for name in ['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']:
        print(f"Processing name: {name}")
        for id, location_ids in enumerate(POINTS):
            input_data['names'] = [name]
            input_data['location_ids'] = location_ids
            print(f'Making request for point group {id + 1} of {len(POINTS)}...')

            if '.csv' in BASE_URL:
                url = BASE_URL + urllib.parse.urlencode(input_data, True)
                # Note: CSV format is only supported for single point requests
                # Suggest that you might append to a larger data frame
                data = pd.read_csv(url, skiprows=2)

                data["DNI(KWH)"] = data["DNI"] / 1000

                data.to_csv("data-{}.csv".format(name), index=False)
                print(f'Response data (you should replace this print statement with your processing): {data}')
                # You can use the following code to write it to a file
                # data.to_csv('SingleBigDataPoint.csv')
            print(f'Processed')

if __name__ == "__main__":
    main()