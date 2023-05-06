# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:47:49 2023

@author: hayoshiz
"""

# import module
import pandas as pd

#%%
## This section aims to create list of MFN tariff rate and EPA tariff rate for each tariff line.

# initialize empty dictionary to store each sheet in a excel file of the information for Japan's MFN and EPA tariff for each tariff line.
jp_tariff_sheets = {}

# initialize empty dataframe for storing MFN and EPA tariff for each tariff line
master_jp_tariff = pd.DataFrame()

# read the excel file and merge as one dataframe 'master_jp_tariff'
num = [1,2,3]
for var in num:
    jp_tariff_sheets[f'DutyDetails_{var}'] = pd.read_excel('../02_Raw/Japan_tariff.xlsx',sheet_name=f'DutyDetails_{var}',usecols=['TL','TLS','Duty Type/Code','AV Duty Rate','Duty Nature'],dtype={'TL':str,'TLS':str,'Duty Type/Code':str,'AV Duty Rate':float,'Duty Nature':str})
    master_jp_tariff = pd.concat([master_jp_tariff,jp_tariff_sheets[f'DutyDetails_{var}']])

# filter out the data to tariff line with AV duty rate, not specific duty rate.
master_jp_tariff = master_jp_tariff[master_jp_tariff['Duty Nature']=='A']
# check to see if 'AV duty rate' has data and 'Duty Nature' is only A
#print(master_jp_tariff['Duty Nature'].value_counts())
#print(master_jp_tariff['AV Duty Rate'].value_counts())

# filter out the minor tariff lines beyond 9 digit to simplify the definition of tariff margin of a tariff line.
master_jp_tariff = master_jp_tariff[(master_jp_tariff['TLS']=="00'") | (master_jp_tariff['TLS']=="  ")]
# check to see if 'TLS' is only '00'' or ''.
#print(master_jp_tariff['TLS'].value_counts())

# drop the unnecessary columns
master_jp_tariff = master_jp_tariff.drop(columns=['TLS','Duty Nature'])

# drop duplicates
master_jp_tariff = master_jp_tariff.drop_duplicates(keep='first',subset=['TL','Duty Type/Code'])

# filter out tariffs for GSP and LDC.
master_jp_tariff = master_jp_tariff[(master_jp_tariff['Duty Type/Code']!="40'") & (master_jp_tariff['Duty Type/Code']!="50'")]

# delete the ' in the end of the HS code
master_jp_tariff['TL'] = master_jp_tariff['TL'].str[:-1]

#%%
## The data is now set.
## This section aims to calculate Tariff Margin
## Tariff Margin = MFN tariff rate - EPA tariff rate.

# Create a function to calculate the tariff margin.
def calculate_tariffmargin(group):
    if "03'" in group['Duty Type/Code'].values:
        group['Tariff Margin'] = group[group['Duty Type/Code'] == "03'"]['AV Duty Rate'].iloc[0] - group['AV Duty Rate']
    elif "02'" in group['Duty Type/Code'].values:
        group['Tariff Margin'] = group[group['Duty Type/Code'] == "02'"]['AV Duty Rate'].iloc[0] - group['AV Duty Rate']
    else:
        group['Tariff Margin'] = 'not AV Duty'
    return group

# Group by tariff line and apply the function
master_jp_tariff = master_jp_tariff.groupby('TL').apply(calculate_tariffmargin)

# filter out record to that is either EPA tariff rate or MFN tariff rate is not AV duty, a specific duty
master_jp_tariff = master_jp_tariff[master_jp_tariff['Tariff Margin'] != 'not AV Duty']

#%%
# export as pickle
master_jp_tariff.to_pickle('../03_Output/jp_tariff_margin.pkl')

# export as csv file
#master_jp_tariff.to_csv('../03_Output/jp_tariffmargin.csv',index=False) 







