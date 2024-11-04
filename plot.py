import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Function to parse the duration text to minutes
def parse_duration(duration_text):
    parts = duration_text.split()
    if 'hour' in parts:
        hours = int(parts[0])
        minutes = int(parts[2])
        return hours * 60 + minutes
    else:
        return int(parts[0])

# Read the CSV files
data_to_work = pd.read_csv('commute_times_to_work.csv')
data_to_home = pd.read_csv('commute_times_to_home.csv')

# Convert the 'Date' and 'Time' columns to datetime
data_to_work['Datetime'] = pd.to_datetime(data_to_work['Date'].astype(str) + ' ' + data_to_work['Time'].astype(str))
data_to_home['Datetime'] = pd.to_datetime(data_to_home['Date'].astype(str) + ' ' + data_to_home['Time'].astype(str))

# Parse the 'Duration' column to numeric values
data_to_work['Duration (minutes)'] = data_to_work['Duration'].apply(parse_duration)
data_to_home['Duration (minutes)'] = data_to_home['Duration'].apply(parse_duration)

# Set the 'Datetime' as the index
data_to_work.set_index('Datetime', inplace=True)
data_to_home.set_index('Datetime', inplace=True)

# Plotting the data
plt.figure(figsize=(12, 6))

plt.plot(data_to_work.index, data_to_work['Duration (minutes)'], label='To Work', marker='o', linestyle='-')
plt.plot(data_to_home.index, data_to_home['Duration (minutes)'], label='To Home', marker='x', linestyle='-')

plt.xlabel('Time')
plt.ylabel('Duration (minutes)')
plt.title('Commute Times Over the Day')
plt.legend()
plt.grid(True)

# Customizing the time format on the x-axis
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
# Rotate the x-axis labels for better readability
plt.gcf().autofmt_xdate()

# Add a secondary x-axis to show the date
secax = ax.secondary_xaxis(-0.2)  # Position the secondary axis below the primary x-axis
secax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %b %d'))

plt.show()
