import pandas as pd

ev_solar_area = 16.7225
cambus_area = 24.8171891

def to_float(x):
    try:
        return float(x)
    except ValueError:
        return x

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



if __name__ == '__main__':
    main()
