# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:33:13 2023

@author: hayoshiz
"""

# import module
import pandas as pd

#%%
# This section aims to create a dataframe 'master_jp_epa' for Japan's EPA imports in 2012 to 2021.
# Because the raw data file for Japn's EPA import is seperated by year, it needs to be merged into one dataframe.
# It is merged as wide data to match with the data structure for total import dataframe 'master_jp_im'.

# initialize empty dictionary to store files
jp_epa_files = {}

# initialize empty dataframe to store master EPA datas
master_jp_epa = pd.DataFrame(columns=['Region','Country','HS'])

# For EPA import data BEFORE 2020.
# range of data years
years = list(range(2012,2021))

# read files
for year in years:
    jp_epa_files[f'jp_epa_{year}'] = pd.read_excel(f'../02_Raw/Japan_EPA/{year}_EPA.xlsx',usecols=['Region','Country','HS','Value-Year'],dtype={'Region':str,'Country':str,'HS':str,'Value-Year':int})
    jp_epa_files[f'jp_epa_{year}'] = jp_epa_files[f'jp_epa_{year}'].rename(columns={'Value-Year':f'{year}'})
    # groupby and sum because column 'EPA code' will make some TLs record seperated.
    jp_epa_files[f'jp_epa_{year}'] = jp_epa_files[f'jp_epa_{year}'].groupby(['Region','Country','HS'])[f'{year}'].sum()
    master_jp_epa = master_jp_epa.merge(jp_epa_files[f'jp_epa_{year}'],how='outer',on=['Region','Country','HS'])

# For EPA import data AFTER 2021. *Difference between files before 2020 is column 'EPA'; not 'Region'.
# read files
jp_epa_files['jp_epa_2021'] = pd.read_excel('../02_Raw/Japan_EPA/2021_EPA.xlsx',usecols=['EPA','Country','HS','Value-Year'],dtype={'EPA':str,'Country':str,'HS':str,'Value-Year':int})
jp_epa_files['jp_epa_2021'] = jp_epa_files['jp_epa_2021'].rename(columns={'Value-Year':'2021','EPA':'Region'})
# groupby and sum because column 'EPA code' will make some TLs record seperated.
jp_epa_files['jp_epa_2021'] = jp_epa_files['jp_epa_2021'].groupby(['Region','Country','HS'])['2021'].sum()
master_jp_epa = master_jp_epa.merge(jp_epa_files['jp_epa_2021'],how='outer',on=['Region','Country','HS'])
#print(master_jp_epa['_merge'].value_counts())
#master_jp_epa = master_jp_epa.drop(columns='_merge')

# convert the country name from japanese to english
jp_en = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='for epa import',usecols=['Country','Def. (Country name)_en'],dtype=str)
master_jp_epa = master_jp_epa.merge(jp_en,on='Country',how='left',validate='m:1',indicator=True)
print(master_jp_epa['_merge'].value_counts())
master_jp_epa = master_jp_epa.drop(columns=['_merge','Country'])

# rename column name
master_jp_epa = master_jp_epa.rename(columns={'HS':'TL','Def. (Country name)_en':'Country'})

# check if the country has a FTA with Japan
fta_countries = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='FTA Countries',dtype=str)
master_jp_epa = master_jp_epa.merge(fta_countries,left_on='Country',right_on='All Countries',how='left',validate='m:1',indicator=True)
print(master_jp_epa['_merge'].value_counts())
master_jp_epa = master_jp_epa.drop(columns=['_merge','All Countries'])

# filter out countries that no FTA with Japan. 'No FTA' was included in this file because of imports from GSP and LDC countries.
master_jp_epa = master_jp_epa[master_jp_epa['FTA Countries']!='No FTA']
print(master_jp_epa['FTA Countries'].value_counts())

# delete the ' in the beginning of the HS code
master_jp_epa['TL'] = master_jp_epa['TL'].str[1:]

# create a new column with 2 digit HS code
master_jp_epa['HS2'] = master_jp_epa['TL'].str[0:2].astype(str)

# create a new column with section name of HS2
section = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='HS',dtype=str)
# delete the ' in the end of HS2
section['HS2'] = section['HS2'].str[:-1]
master_jp_epa = master_jp_epa.merge(section,on='HS2',how='left',validate='m:1',indicator=True)
print(master_jp_epa['_merge'].value_counts())
master_jp_epa = master_jp_epa.drop(columns='_merge')

# merge the Duty Type/Code
a = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='Duty Type for epa import',dtype=str)
master_jp_epa= master_jp_epa.merge(a,on=['Region','Country'],how='left',validate='m:1',indicator=True)
print(master_jp_epa['_merge'].value_counts())
master_jp_epa = master_jp_epa.drop(columns=['_merge','FTA','Region'])

# merge the tariff margin for each HS code for each EPA
master_jp_tariff = pd.read_pickle('../03_Output/jp_tariff_margin.pkl')
master_jp_epa = master_jp_epa.merge(master_jp_tariff,on=['TL','Duty Type/Code'],validate='m:1',how='left',indicator=True)
print(master_jp_epa['_merge'].value_counts())
master_jp_epa = master_jp_epa.drop(columns='_merge')

# store the datas that the tariff margin is less than zero for later analysis.
master_jp_epa_notariffmargin = master_jp_epa[master_jp_epa['Tariff Margin'] <= 0]

# filter out the HS codes that have Tariff Margin less than zero
master_jp_epa = master_jp_epa[master_jp_epa['Tariff Margin'] > 0]

#%%
# export as pickle
master_jp_epa.to_pickle('../03_Output/jp_epa_im.pkl')

# export as csv file
#master_jp_epa.to_csv('../03_Output/jp_epa_im.csv')

