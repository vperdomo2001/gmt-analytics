import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
    
# all session dataframe
all_ses = pd.read_csv('sessions_Maria_Perdomo-Torres_all_20250710.csv')

# convert date to datetime data type
all_ses['DATE'] = pd.to_datetime(all_ses['DATE'], format='%Y-%m-%d')
# sort by date
all_ses = all_ses.sort_values(by='DATE')

# insurance segment financial analysis 
# assign insurance (payment) to session df
all_clients = pd.read_csv('AllClientsEdited.csv') # get payment method 
# focus on sessions this past year 
all_ses.rename(columns={'NAME': 'FULL_NAME'}, inplace=True) # rename name column 
# print(all_ses.head(20))
ses_year = all_ses[(all_ses['DATE'] >= '2024-07-10') & (all_ses['DATE'] <= '2025-07-10')].copy()
print('Sessions YTD: ' + str(ses_year.shape[0]))
# convert dtype to strings
# no unique id numbers, will have to use names as key 
# strip and uppercase names 
ses_year.FULL_NAME = ses_year.FULL_NAME.astype(str)
ses_year['FULL_NAME'] = ses_year['FULL_NAME'].str.strip().str.upper()
all_clients.FULL_NAME = all_clients.FULL_NAME.astype(str)
all_clients['FULL_NAME'] = all_clients['FULL_NAME'].str.strip().str.upper()
# Keep only one insurance method per person — e.g., the most common or latest
clients_dedup = all_clients.groupby('FULL_NAME')['METHOD'].agg(lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]).reset_index()
# merge method to session df
ses_year = ses_year.merge(clients_dedup, on='FULL_NAME', how='left')

# # do math!
method_counts = ses_year.groupby('METHOD')['LENGTH'].value_counts()
method_counts = method_counts.reset_index(name='COUNT')
# print(method_counts)
# get method rates to compare across segments
method_rates = pd.read_csv('Insurance_Method_Rates.csv') 
method_rates.iloc[12] = method_rates.iloc[12].str.replace("$","")
method_rates.iloc[12,2:5] = method_rates.iloc[12,2:5].astype(float)
# print(method_rates)

# tabluate alma cost 
alma_cost = (method_counts['COUNT'].loc[(method_counts['METHOD'] == 'Alma')]).sum()*method_rates.loc[len(method_rates)-1,'Alma']
alma_cost_f = "{:,}".format(alma_cost)
print('Alma Earnings = $' + str(alma_cost_f))
# alma + eap
alma_eap_cost = (method_counts['COUNT'].loc[(method_counts['METHOD'] == 'Alma')]).sum()*107.82 + (method_counts['COUNT'].loc[(method_counts['METHOD'] == 'EAP')]).sum()*method_rates.loc[len(method_rates)-1,'EAP']
alma_eap_cost_f = "{:,}".format(alma_eap_cost)
print('Alma + EAP Earnings = $'+ str(alma_eap_cost_f))
# headway 
hw_cost = (method_counts['COUNT'].loc[(method_counts['METHOD'] == 'Headway')]).sum()*method_rates.loc[len(method_rates)-1,'Headway']
hw_cost_f = "{:,}".format(hw_cost)
print('Headway Earnings = $'+ str(hw_cost_f))

# # by session length 
# alma_cost = (method_counts['COUNT'].loc[(method_counts['METHOD'] == 'Alma') & (method_counts['LENGTH'] == '60 min')]).sum()*method_rates.loc[len(method_rates)-1,'Alma']
