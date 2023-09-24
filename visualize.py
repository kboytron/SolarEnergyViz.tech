import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3

# daily data

data_daily = pd.read_csv('data/daily_energy_conversion.csv')

data_daily['Date'] = pd.to_datetime(data_daily['Date'])

# Create a lineplot with a yellow line
fig = plt.figure(figsize=(10, 6))
sns.lineplot(data=data_daily, x="Date", y="Energy_conversion", color="yellow")

# Set the title with white color
plt.title('Energy Conversion over Time (Daily)', color='white')

# Setting the label colors to white
plt.xlabel('Date', color='white')
plt.ylabel('Energy Conversion', color='white')

# Setting the tick parameters to have white color
plt.tick_params(colors='white')

# Save the plot as a .png file
plt.savefig('html/plot-daily.png', transparent=True)

# hourly data

data_hourly = pd.read_csv('data/hourly_energy_conversion.csv')

data_hourly['Date'] = pd.to_datetime(data_hourly['Date'])

# Create a lineplot with a yellow line
fig = plt.figure(figsize=(10, 6))
sns.lineplot(data=data_hourly, x="Date", y="Energy_conversion", color="yellow")

# Set the title with white color
plt.title('Energy Conversion over Time (Hourly)', color='white')

# Setting the label colors to white
plt.xlabel('Date', color='white')
plt.ylabel('Energy Conversion', color='white')

# Setting the tick parameters to have white color
plt.tick_params(colors='white')

# Save the plot as a .png file
plt.savefig('html/plot-hourly.png', transparent=True)

