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

# comparison 

# Load the data into a pandas DataFrame
data_compare = pd.read_csv("data/solar_panel_compare.csv")

# Create a line plot for Siliken and Uni Solar Energy Conversion
fig = plt.figure(figsize=(10, 6))
sns.lineplot(data=data_compare, x="Month", y="Siliken_energy_conversion", color="yellow", label="Siliken")
sns.lineplot(data=data_compare, x="Month", y="Uni_solar_energy_conversion", color="orange", label="Uni Solar")

# Set the title with white color
plt.title('Energy Conversion Over Time', color='white')

# Setting the label colors to white
plt.xlabel('Month', color='white')
plt.ylabel('Energy Conversion', color='white')

# Setting the tick parameters to have white color
plt.tick_params(colors='white')

# Adding the legend with white color
plt.legend(loc='upper right', facecolor='black', edgecolor='white', fontsize='medium', framealpha=1, labelcolor='white')

# Save the plot as a .png file with a transparent background
plt.savefig('html/plot-energy_conversion.png', transparent=True)