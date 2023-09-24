import pandas as pd
from prophet import Prophet

# Combine data from all files into one DataFrame
all_data = []

for year in range(2011, 2022):
    file_name = "data/data-{}.csv".format(year)
    data = pd.read_csv(file_name)
    all_data.append(data)

combined_data = pd.concat(all_data, ignore_index=True)

# Prepare the data for Prophet
combined_data['ds'] = pd.to_datetime(combined_data[['Year', 'Month', 'Day', 'Hour', 'Minute']])
combined_data = combined_data[['ds', 'DNI(KWH)']]
combined_data.rename(columns={'DNI(KWH)': 'y'}, inplace=True)

# Initialize and fit the model
model = Prophet(yearly_seasonality=True, daily_seasonality=True)
model.fit(combined_data)

# Create a DataFrame for future dates to predict (2022 and 2023)
future = model.make_future_dataframe(periods=2*365*24, freq='H')

# Predict
forecast = model.predict(future)

# Visualize the forecast
fig = model.plot(forecast)

# Filter the forecast for 2022 values
forecast_2022 = forecast[forecast['ds'].dt.year == 2022]
forecast_2023 = forecast[forecast['ds'].dt.year == 2023]  # for 2023

# Extract Year, Month, Day, Hour from 'ds' column for 2022
forecast_2022['Year'] = forecast_2022['ds'].dt.year
forecast_2022['Month'] = forecast_2022['ds'].dt.month
forecast_2022['Day'] = forecast_2022['ds'].dt.day
forecast_2022['Hour'] = forecast_2022['ds'].dt.hour
forecast_2022['Minute'] = forecast_2022['ds'].dt.minute

# Extract Year, Month, Day, Hour from 'ds' column for 2023
forecast_2023['Year'] = forecast_2023['ds'].dt.year
forecast_2023['Month'] = forecast_2023['ds'].dt.month
forecast_2023['Day'] = forecast_2023['ds'].dt.day
forecast_2023['Hour'] = forecast_2023['ds'].dt.hour
forecast_2023['Minute'] = forecast_2023['ds'].dt.minute

# Select only the required columns and rename the 'yhat_upper' column for 2022
final_df_2022 = forecast_2022[['Year', 'Month', 'Day', 'Hour', 'Minute', 'yhat_upper']]
final_df_2022.rename(columns={'yhat_upper': 'DNI(KWH)'}, inplace=True)

# Select only the required columns and rename the 'yhat_upper' column for 2023
final_df_2023 = forecast_2023[['Year', 'Month', 'Day', 'Hour', 'Minute', 'yhat_upper']]
final_df_2023.rename(columns={'yhat_upper': 'DNI(KWH)'}, inplace=True)

# Save to CSV
final_df_2022.to_csv('data/data-2022.csv', index=False)
final_df_2023.to_csv('data/data-2023.csv', index=False)
