import pandas as pd

ev_solar_area = float(16.7225)
cambus_area = float(24.8171891)

def to_float(x):
    try:
        return float(x)
    except ValueError:
        return x

def energy_conversion(date,radiance,kwh,panel_size):
    return kwh/(radiance*panel_size) #assuming silica conductor


def main():
    df = pd.read_csv("data/solar_data.csv", skiprows=1)

    # Convert the Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert numeric strings to float, while keeping non-numeric values as strings
    df['EL_Solar_BusBarn_Total_KW'] = df['EL_Solar_BusBarn_Total_KW'].apply(to_float)
    df['EL_Solar_BusBarn_KWH_Dtot'] = df['EL_Solar_BusBarn_KWH_Dtot'].apply(to_float)

    # Find the unique days where EL_Solar_BusBarn_KWH_Dtot is "Calc Failed"
    failed_dates = df[df['EL_Solar_BusBarn_KWH_Dtot'] == 'Calc Failed']['Date'].dt.date.unique()

    for date in failed_dates:
        # Calculate the total KW for the specific date
        total_kw = df[df['Date'].dt.date == date]['EL_Solar_BusBarn_Total_KW'].sum()
        
        # Update the value in the EL_Solar_BusBarn_KWH_Dtot column for the given date
        df.loc[(df['Date'].dt.date == date) & (df['EL_Solar_BusBarn_KWH_Dtot'] == 'Calc Failed'), 'EL_Solar_BusBarn_KWH_Dtot'] = total_kw
    
    # For rows with "No Good Data", calculate the values
    no_good_rows = df[df['EL_Solar_BusBarn_Total_KW'] == "[-11059] No Good Data For Calculation"]
    for index, row in no_good_rows.iterrows():
        date = row['Date'].date()
        
        # Calculate the day's total KW
        day_total_kw = float(df[df['Date'].dt.date == date]['EL_Solar_BusBarn_KWH_Dtot'].iloc[0])
        
        # Get valid KW data for that day
        valid_kw = df[(df['Date'].dt.date == date) & (df['EL_Solar_BusBarn_Total_KW'] != "[-11059] No Good Data For Calculation")]['EL_Solar_BusBarn_Total_KW'].sum()
        
        # Calculate the total value to be distributed across the "No Good Data" rows
        to_be_distributed = float(day_total_kw) - valid_kw
        
        # Count the "No Good Data" rows for that day
        no_good_count = len(df[(df['Date'].dt.date == date) & (df['EL_Solar_BusBarn_Total_KW'] == "[-11059] No Good Data For Calculation")])
        
        # Calculate value per "No Good Data" row
        value_per_row = to_be_distributed / no_good_count
        
        # Update the "No Good Data" rows with the calculated value
        df.loc[index, 'EL_Solar_BusBarn_Total_KW'] = value_per_row

    df.to_csv("data/cleaned_solar.csv", index=False)

    # <<<<<< Data Cleaning and Restructuring >>>>>>
    # Cleaned Data Frame Restructuring - Hourly/Daily
    hourly_df = df.iloc[:,0:2]
    hourly_df = hourly_df.rename(columns={'EL_Solar_BusBarn_Total_KW': 'Total_KW'})
    hourly_df['Date'] = hourly_df['Date'].astype(str)

    # Split the datetime column
    datetime_parts = hourly_df['Date'].str.split(' ', expand=True)
    hourly_df['Date'] = datetime_parts[0]
    hourly_df['Hour'] = datetime_parts[1].str[:2]
    hourly_df = hourly_df[['Date', 'Hour', 'Total_KW']]

    # Convert the dates to numbers
    """daily_df = df.iloc[:, 3:]
    daily_df.dropna(inplace=True)
    daily_df = daily_df.rename(columns={'Date.1': 'Date'})
    daily_df = daily_df.rename(columns={'EL_Solar_BusBarn_KWH_Dtot': 'KWH_Dtot'})
    daily_df['Date'] = pd.to_datetime(daily_df['Date'], format='%d-%b-%y %H:%M:%S', dayfirst=True)
    daily_df['Date'] = daily_df['Date'].dt.strftime('%d-%m-%y')
    daily_df['Date'] = pd.to_datetime(daily_df['Date'], format='%d-%m-%y')
    daily_df['Date'] = daily_df['Date'].dt.strftime('%Y-%m-%d')"""

    # Combine all radiance csv to one dataframe
    csv_files = ["data-2011.csv","data-2012.csv","data-2013.csv" ,"data-2014.csv"
    ,"data-2015.csv","data-2016.csv","data-2017.csv","data-2018.csv","data-2019.csv"
    ,"data-2020.csv", "data-2021.csv" , "data-2022.csv" , "data-2023.csv"]
    combined_irradiance_df = pd.DataFrame()
    dfs = []
    for csv_file in csv_files:
        temp_df = pd.read_csv("data/"+csv_file)

        if not dfs:
            dfs.append(temp_df)
        else:
            dfs.append(temp_df.iloc[1:])


    combined_irradiance_df = pd.concat(dfs, ignore_index=True)

    # Combine 'Year', 'Month', and 'Day' columns into a single 'Date' column
    combined_irradiance_df['Date'] = pd.to_datetime(
        combined_irradiance_df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1),
        format='%Y-%m-%d'
    )

    # Reorder the columns to have 'Date' as the first column and keep other columns
    column_order = ['Date'] + [col for col in combined_irradiance_df.columns if col != 'Date']
    combined_irradiance_df = combined_irradiance_df[column_order]
    combined_irradiance_df = combined_irradiance_df.drop(['Year', 'Month', 'Day'], axis=1)

    # <<<<<< Energy Conversion Calculations >>>>>>
    combined_irradiance_df.to_csv("data/combined_irradiance.csv", index=False)
    # hourly energy conversion calculations
    # Convert the 'Hour' column in hourly_df to strings to match the data type
    hourly_df['Date'] = hourly_df['Date'].astype(str)
    hourly_df['Hour'] = hourly_df['Hour'].astype(int)
    hourly_df['Hour'] = hourly_df['Hour'].astype(str)
    combined_irradiance_df = combined_irradiance_df.astype(str)
    merged_df = pd.merge(hourly_df, combined_irradiance_df, on=['Date', 'Hour'], how='inner')

    merged_df['Total_KW'] = merged_df['Total_KW'].astype(float)  # Calculate 'Energy_conversion' by dividing 'DNI(KWH)' by 'Total_KW' with a check for zero division
    merged_df['Energy_conversion'] = merged_df.apply(
        lambda row: float(row['Total_KW']) / (float(row['DNI(KWH)']) * ev_solar_area) if float(row['DNI(KWH)']) != 0 else 0, axis=1)

    # Select and reorder columns in the final DataFrame
    hourly_df = merged_df[['Date', 'Hour', 'Total_KW','DNI(KWH)' ,'Energy_conversion']]
    hourly_df['Energy_conversion'].fillna(0, inplace=True)
    hourly_df["DNI(KWH)"] = hourly_df['DNI(KWH)'].astype(float)
    # Remove rows where 'DNI(KWH)' is greater than 100
    hourly_df = hourly_df[hourly_df['DNI(KWH)'] <= 100]
    hourly_df = hourly_df[hourly_df['Total_KW'] <= 100]
    hourly_df = hourly_df[hourly_df['Energy_conversion'] <= 15]
    hourly_df.reset_index(drop=True, inplace=True)
    hourly_df.to_csv("data/hourly_energy_conversion.csv", index=False)
    print("Computed and saved hourly energy conversions")

    # Yearly calculations
    grouped = hourly_df.groupby('Date')
    daily_df = grouped[['Total_KW']].sum().reset_index() #creating modified daily_df


    combined_irradiance_df["DNI"] = combined_irradiance_df["DNI"].astype(float)
    combined_irradiance_df["DNI(KWH)"] = combined_irradiance_df["DNI(KWH)"].astype(float)
    grouped = combined_irradiance_df.groupby('Date')
    daily_combined_irradiance_df = grouped[['DNI', 'DNI(KWH)']].sum().reset_index() #adds up hourly irradiance data into days
    daily_merged_df = pd.merge(daily_df, daily_combined_irradiance_df, on=['Date'], how='inner')
    daily_merged_df['Total_KW'] = daily_merged_df['Total_KW'].astype(float)
    daily_merged_df['Energy_conversion'] = daily_merged_df.apply(
        lambda row: float(row['Total_KW']) / (float(row['DNI(KWH)']) * ev_solar_area) if float(
            row['DNI(KWH)']) != 0 else 0, axis=1)

    daily_df = daily_merged_df[['Date', 'Total_KW','DNI(KWH)','Energy_conversion']]
    daily_df = daily_df[daily_df['Energy_conversion'] <= 15]
    daily_df.reset_index(drop=True, inplace=True)
    daily_df.to_csv("data/daily_energy_conversion.csv", index=False)
    print("Completed and saved Daily energy conversions")

    # <<<<<< Comparing Both Solar Panels >>>>>>>
    #create monthly data
    daily_df = daily_df[daily_df['Date'].str.startswith('2023')]
    daily_df['Year'] = pd.to_datetime(daily_df['Date']).dt.year
    daily_df['Month'] = pd.to_datetime(daily_df['Date']).dt.strftime('%b %Y')  # Format as "Jan 2023"
    grouped = daily_df.groupby(['Year', 'Month'])
    monthly_df = grouped[['Total_KW']].sum().reset_index() # Calculate sums for 'Total_KW'
    monthly_df['Month'] = pd.to_datetime(monthly_df['Month'], format='%b %Y') # Convert 'Month' back to datetime format for sorting

    # Sort the DataFrame by 'Month' in ascending order
    monthly_df = monthly_df.sort_values(by='Month')
    monthly_df = monthly_df.drop("Year", axis=1)
    monthly_df["Total_KW"] = monthly_df["Total_KW"].astype(float)
    #create monthly list of irradiance
    siliken_solar_radiance = [3.41,4.0,4.70,5.10,5.54,5.94,6.25,5.95,5.44]
    uni_solar_radiance = [2.53,3.22,4.24,5.01,5.82,6.41,6.59,5.96,4.98]

    #Apply the formula to calculate energy conversion
    monthly_df['Siliken_energy_conversion'] = monthly_df['Total_KW'] / (siliken_solar_radiance)
    monthly_df['Siliken_energy_conversion'] = monthly_df['Siliken_energy_conversion'] / ev_solar_area
    monthly_df['Uni_solar_energy_conversion'] = monthly_df['Total_KW'] / (uni_solar_radiance)
    monthly_df['Uni_solar_energy_conversion'] = monthly_df['Uni_solar_energy_conversion'] / cambus_area

    #save the csv
    monthly_df['Month'] = pd.to_datetime(monthly_df['Month']).dt.strftime('%b-%Y')
    monthly_df.to_csv("data/solar_panel_compare.csv", index=False)
    print(monthly_df)

if __name__ == '__main__':
    main()
