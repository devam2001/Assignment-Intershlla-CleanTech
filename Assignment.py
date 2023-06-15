import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from numpy.random import random

file = "C:/Users/devam/OneDrive/Desktop/CleanTech/Assignment_Dataset.xlsx"
df = pd.read_excel(file)
df['PR_MA_30'] = df['PR'].rolling(window=30).mean()

budget_values = [73.9]
for i in range(1, len(df)):
    year = pd.to_datetime(df['Date'][i]).year
    budget_values.append(round(budget_values[0] * (0.992 ** (year - 2019)), 1))

budget_decrease = [0]
for i in range(1, len(budget_values)):
    decrease = (budget_values[i] - budget_values[i-1])/budget_values[i-1]
    budget_decrease.append(round(decrease, 4)*100)

fig, ax = plt.subplots(figsize=(10, 6))
colors = np.select([df['GHI'] < 2, (df['GHI'] >= 2) & (df['GHI'] < 4),
                    (df['GHI'] >= 4) & (df['GHI'] < 6), df['GHI'] >= 6],
                   ['navy', 'lightblue', 'orange', 'brown'])

# Create scatter plot legends
# legend_elements = [
#     plt.Line2D([0], [0], marker='D', color='navy', markersize=4, label='< 2 GHI'),
#     plt.Line2D([0], [0], marker='D', color='lightblue', markersize=4, label='2-4 GHI'),
#     plt.Line2D([0], [0], marker='D', color='orange', markersize=4, label='4-6 GHI'),
#     plt.Line2D([0], [0], marker='D', color='brown', markersize=4, label='>= 6 GHI')
# ]
# ax.legend(handles=legend_elements, loc='center')

colors1 = ['navy', 'lightblue', 'orange', 'brown']

ny = plt.scatter(random(10), random(10), marker='D', color=colors1[0])
lb = plt.scatter(random(10), random(10), marker='D', color=colors1[1])
ora= plt.scatter(random(10), random(10), marker='D', color=colors1[2])
br = plt.scatter(random(10), random(10), marker='D', color=colors1[3])

plt.legend((ny, lb, ora, br),
           ('< 2 GHI', '2-4 GHI', '4-6 GHI', '>= 6 GHI'),
           scatterpoints=1,
           loc='upper center',
           ncol=3,
           fontsize=4)
colors = np.select([df['GHI'] < 2, (df['GHI'] >= 2) & (df['GHI'] < 4),
                    (df['GHI'] >= 4) & (df['GHI'] < 6), df['GHI'] >= 6],
                   ['navy', 'lightblue', 'orange', 'brown'])

ax.scatter(df['Date'], df['PR'], c=colors, alpha=1, marker='D', s = 10)

ax.plot(df['Date'], budget_values, color='darkgreen', label='Target Budget Yield Performance Ratio [1Y-73.9%,2Y-73.3%,3Y-72.7%]')
ax.plot(df['Date'], df['PR_MA_30'], color='red', label='30-d moving average of PR')


ax.set_xlabel('Date')
ax.set_ylabel('Performance Ratio')
title_font = fm.FontProperties(weight='bold')
ax.set_title('Performance Ratio vs Irradiation \n From 2019-07-01 to 2022-03-24', fontproperties=title_font)
ax.legend(loc='lower left')
ax.set_xlim(pd.Timestamp('2019-07-01'), pd.Timestamp('2022-01-01'))
ax.set_yticks(range(0, min(int(df['PR'].max()) + 10, 100), 10))

# Add the legend for the average PR values in the bottom right corner
last_7_days = df['PR'].rolling(window=7).mean().tail(1).values[0]
last_30_days = df['PR'].rolling(window=30).mean().tail(1).values[0]
last_60_days = df['PR'].rolling(window=60).mean().tail(1).values[0]
last_90_days = df['PR'].rolling(window=90).mean().tail(1).values[0]
last_365_days = df['PR'].rolling(window=365).mean().tail(1).values[0]
average_pr_lifetime = df['PR'].mean()

legend_text = f'Average PR last 7-d: {last_7_days:.2f} %\nAverage PR last 30-d: {last_30_days:.2f} %\nAverage PR last 60-d: {last_60_days:.2f} %\nAverage PR last 90-d: {last_90_days:.2f} %\nAverage PR last 365-d: {last_365_days:.2f} %\nAverage PR lifetime: {average_pr_lifetime:.2f} %'
plt.text(0.67, 0.16, legend_text, transform=plt.gcf().transFigure, fontsize=10)

# Set the y-axis range
ax.set_ylim(0, 100)

# Set the date format
date_format = mdates.DateFormatter('%b/%y')
ax.xaxis.set_major_formatter(date_format)

# Add gridlines
ax.grid(True)

plt.show()
