import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# all clients dataframe
all_clients = pd.read_csv('AllClientsExport_2025-06-21.csv')

# # separate labels into new columns
# referral source column 
def extract_referral_source(label_str):
    label_str = str(label_str)  # Force everything to string (even NaN becomes 'nan')
    # skip invalid entries
    if label_str.lower() == 'nan' or label_str.strip() == '':
        return None
    labels = [label.strip() for label in label_str.split(',')]
    for label in labels:
        if '_ref' in label.lower():
            return label.rsplit('_', 1)[0]
    # Special case: Psychology Today
    if any('psychology today' in label.lower() for label in labels):
        return 'Psychology Today'
    return None
all_clients['REFERRAL_SOURCE'] = all_clients['LABELS'].apply(extract_referral_source)

# method column 
def extract_method(label_str):
    label_str = str(label_str)
    # skip invalid entries 
    if label_str.lower() == 'nan' or label_str.strip() == '':
        return None
    # go through labels and create list of labels
    labels = [label.strip() for label in label_str.split(',')]
    for label in labels:
        if 'eap' in label.lower():
            return 'EAP'
        if 'alma' in label.lower() and 'alma_ref' not in label.lower() and 'EAP' not in labels:
            return 'Alma'
        if 'headway' in label.lower():
            return 'Headway'
        if 'aws' in label.lower():
            return 'aws'
        if 'cash-pay' in label.lower():
            return 'Cash-Pay'
    return None 
all_clients['METHOD'] = all_clients['LABELS'].apply(extract_method)

# payment tier column 
def extract_tier(label_str):
    label_str = str(label_str)
    # skip invalid entries 
    if label_str.lower() == 'nan' or label_str.strip() == '':
        return None
    # go through labels and create list of labels
    labels = [label.strip() for label in label_str.split(',')]
    for label in labels:
        if 'tier' in label.lower():
            return label
    # Special case: sliding scale
    if any('sliding scale' in label.lower() for label in labels):
        return 'Sliding Scale'
all_clients['TIER'] = all_clients['LABELS'].apply(extract_tier)

# add full name column 
all_clients['FULL_NAME'] = all_clients[['CLIENT_LAST_NAME','CLIENT_FIRST_NAME']].agg(', '.join, axis=1)

# # filter to active clients 
active_clients = all_clients[all_clients['STATUS'] == 'Active'].copy()
# print(active_clients.shape)
# print(all_clients.shape)
# print(active_clients.columns.tolist())


# how many clients in each state 
print('##################################')
print('CLIENT COUNT SUMMARY')
print('----------------------------------')
print('ACTIVE')
print('Current Active Clients: ' + str(len(active_clients)))
state_count_act = active_clients['ADDRESS_STATE'].value_counts()
state_percent_act = round(active_clients['ADDRESS_STATE'].value_counts()/len(active_clients)*100)
print('Active Clients by State: \n')
print(pd.concat([state_count_act,state_percent_act], axis=1, keys=['Total','Percentage (%)']))
print('- - - - - - - - - - - - - -')
print('ALL')
print('All Client Count: ' + str(len(active_clients)))
state_count_all = all_clients['ADDRESS_STATE'].value_counts()
print('All Clients by State: \n')
state_percent_all = round(all_clients['ADDRESS_STATE'].value_counts()/len(all_clients)*100)
print(pd.concat([state_count_all,state_percent_all], axis=1, keys=['Total','Percentage (%)']))
print('##################################')


print('City Count \n' + str(active_clients['ADDRESS_CITY'].value_counts()))
print('Gender Count: \n' + str(active_clients['GENDER'].value_counts()))

# average age of client
all_clients['DATE_OF_BIRTH'] = pd.to_datetime(all_clients['DATE_OF_BIRTH'])
all_clients['AGE'] = (datetime.today() - all_clients['DATE_OF_BIRTH'])/np.timedelta64(1, 'D')
all_clients['AGE'] = all_clients['AGE']/365.25 # convert to years 
all_clients['AGE'] = all_clients['AGE'].astype(int)

active_clients['DATE_OF_BIRTH'] = pd.to_datetime(active_clients['DATE_OF_BIRTH'])
active_clients['AGE'] = (datetime.today() - active_clients['DATE_OF_BIRTH'])/np.timedelta64(1, 'D')
active_clients['AGE'] = active_clients['AGE']/365.25 # convert to years
active_clients['AGE'] = active_clients['AGE'].astype(int)

print('##################################')
print('CLIENT AGE SUMMARY')
print('----------------------------------')
print('ACTIVE')
print('Average Age of Active Clients: ' + str(round(np.mean(active_clients['AGE']),0)))
print('Median Age of Active Clients: ' + str(round(np.median(active_clients['AGE']),0)))
print('- - - - - - - - - - - - - -')
print('ALL')
print('Average Age of All Clients: ' + str(round(np.mean(all_clients.AGE),0)))
print('Median Age of All Clients: ' + str(round(np.median(all_clients['AGE']),0)))
print('##################################')

# how many clients using insurance 
print('##################################')
print('CLIENT INSURANCE SUMMARY')
print('----------------------------------')
print('ACTIVE')
ins_count_act = active_clients['METHOD'].value_counts(dropna=False)
ins_perc_act = active_clients['METHOD'].value_counts(dropna=False,normalize=True).mul(100).round(1).astype(str)
print('Active Client by Payment Method:')
print(pd.concat([ins_count_act,ins_perc_act], axis=1, keys=['Total','Percentage (%)']))
print('##################################')

# how many clients are in each tier
print('##################################')
print('CLIENT TIER SUMMARY')
print('----------------------------------')
print('ACTIVE')
tier_count_act = active_clients['TIER'].value_counts(dropna=False)
tier_perc_act = active_clients['TIER'].value_counts(dropna=False,normalize=True).mul(100).round(1).astype(str)
print('Active Client by Tier:')
print(pd.concat([tier_count_act,tier_perc_act], axis=1, keys=['Total','Percentage (%)']))
print('##################################')

# how did clients hear about you 
print('##################################')
print('CLIENT REFERRAL SOURCE SUMMARY')
print('----------------------------------')
print('ACTIVE')
ref_count_act = active_clients['REFERRAL_SOURCE'].value_counts(dropna=False)
ref_perc_act = active_clients['REFERRAL_SOURCE'].value_counts(dropna=False,normalize=True).mul(100).round(1).astype(str)
print('Active Client by Referral Source:')
print(pd.concat([ref_count_act,ref_perc_act], axis=1, keys=['Total','Percentage (%)']))
print('##################################')

# export to CSV w new columns 
# all_clients.to_csv('AllClientsEdited.csv')