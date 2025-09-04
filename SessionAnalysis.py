import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
    
# all session dataframe
all_ses = pd.read_csv('sessions_Maria_Perdomo-Torres_all_20250710.csv')

# how many sessions total 
print('Total sessions: ' + str(all_ses.shape[0]))

# time series analysis
# convert date to datetime data type
all_ses['DATE'] = pd.to_datetime(all_ses['DATE'], format='%Y-%m-%d')
# sort by date
all_ses = all_ses.sort_values(by='DATE')

# calculate cumulative number of sessions
all_ses['NUMBER_OF_SESSIONS'] = range(len(all_ses))

# plot - number of sessions over time
sns.lineplot(all_ses, x='DATE',y='NUMBER_OF_SESSIONS')
plt.xlabel('Time')
plt.ylabel('Number of Sessions')
plt.title('Cumulative Sessions Over Time')
plt.style.use('bmh')
plt.show()


# # how many sessions per month? 
# format and filter to be able to group and plot by month
all_ses.index = all_ses['DATE']
# print(all_ses.head())
ses_month = all_ses['STATUS'].resample('ME').count()
ses_month = ses_month.to_frame(name='SESSIONS')
ses_month['MONTH'] = ses_month.index.strftime("%b")
ses_month['YEAR'] = ses_month.index.year
ses_month['DATE'] = ses_month.index
ses_month = ses_month[(ses_month['YEAR'] <= 2025) & (ses_month['YEAR'] >= 2022)]
ses_month = ses_month[ses_month['DATE'] < '2025-07-01']


# plot number of sessions per month 
l = sns.lineplot(ses_month, x='DATE',y='SESSIONS')
plt.xlabel('Time')
plt.ylabel('Number of Sessions')
plt.title('Sessions per Month Over Time')
# vertical lines 
y2023 = pd.to_datetime('2023-01-01')
plt.axvline(x=y2023,linestyle='--',color='black',linewidth=0.5)
y2024 = pd.to_datetime('2024-01-01')
plt.axvline(x=y2024,linestyle='--',color='black',linewidth=0.5)
y2025 = pd.to_datetime('2025-01-01')
plt.axvline(x=y2025,linestyle='--',color='black',linewidth=0.5)
plt.show()

# grouped bar plot of sessions per month 
sns.barplot(
    data=ses_month,
    x='MONTH',
    y='SESSIONS',
    hue='YEAR'
)
plt.show()

# is there seasonality?
# line plot of sessions per month 
sns.catplot(data=ses_month, x='MONTH',y='SESSIONS',hue='YEAR',kind='point',palette='muted')
plt.xlabel('Month')
plt.ylabel('Number of Sessions')
plt.title('Sessions per Month')
plt.subplots_adjust(top=0.9)
plt.show()