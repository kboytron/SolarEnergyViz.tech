import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3

data = pd.read_csv('data/hourly_energy_conversion.csv')

data['Date'] = pd.to_datetime(data['Date'])

fig = plt.figure(figsize=(10, 6))
sns.lineplot(data=data, x="Date", y="Energy_conversion")
plt.title('Total_KW over Time')

plt.savefig('data/plot.png')

# Convert the figure to HTML
html_str = mpld3.fig_to_html(fig)

with open('html/plot.html', 'w') as f:
    # Write the HTML string to the file
    f.write(html_str)
