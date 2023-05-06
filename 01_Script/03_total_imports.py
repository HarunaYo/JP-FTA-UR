# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:33:13 2023

@author: hayoshiz
"""

# import module
import pandas as pd

#%%
## This section aims to create a dataframe 'master_jp_im' for Japan's total imports in 2012 to 2021.

# read file
master_jp_im = pd.read_excel('../02_Raw/Japan_imports.xlsx',dtype={'Trade Partner':str,'Tariff Line Code':str})
#2012:int,2013:int,2014:int,2015:int,2016:int,2017:int,2018:int,2019:int,2020:int,2021:int

# drop the unnecessary columns
master_jp_im = master_jp_im.drop(columns=['Reporter','Trade Direction'])

# convert the import value into thousand Japanese yen
years = list(range(2012,2022))
for year in years:
    master_jp_im[year] = master_jp_im[year] / 1000

# Add leading zeros to HS codes to make it 9 digit.
master_jp_im['Tariff Line Code'] = master_jp_im['Tariff Line Code'].apply(lambda x: x.zfill(9))

# convert the country name from japanese to english
jp_en = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='for total import',dtype=str)
#print(jp_en.columns)
#print(master_jp_im.columns)
master_jp_im = master_jp_im.merge(jp_en,on='Trade Partner',how='left',validate='m:1',indicator=True)
print(master_jp_im['_merge'].value_counts())
master_jp_im = master_jp_im.drop(columns=['_merge','Trade Partner'])

# rename column name
master_jp_im = master_jp_im.rename(columns={'Tariff Line Code':'TL','Trade Partner_en':'Country',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020',2021:'2021'})

# check if the country has a FTA with Japan
fta_countries = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='FTA Countries',dtype=str)
master_jp_im = master_jp_im.merge(fta_countries,left_on='Country',right_on='All Countries',how='left',validate='m:1',indicator=True)
print(master_jp_im['_merge'].value_counts())
master_jp_im = master_jp_im.drop(columns=['_merge','All Countries'])

# filter out countries that no FTA with Japan.
master_jp_im = master_jp_im[master_jp_im['FTA Countries']!='No FTA']
print(master_jp_im['FTA Countries'].value_counts())

# create a new column with 2 digit HS code
master_jp_im['HS2'] = master_jp_im['TL'].str[0:2].astype(str)

# create a new column with section name of HS2
section = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='HS',dtype=str)
# delete the ' in the end of HS2
section['HS2'] = section['HS2'].str[:-1]
master_jp_im = master_jp_im.merge(section,on='HS2',how='left',validate='m:1',indicator=True)
print(master_jp_im['_merge'].value_counts())
master_jp_im = master_jp_im.drop(columns='_merge')

# merge the Duty Type/Code
b = pd.read_excel('../02_Raw/key_list.xlsx',sheet_name='Duty Type for tot import',dtype=str)
master_jp_im = master_jp_im.merge(b,on='Country',how='outer',validate='m:m',indicator=True)
print(master_jp_im['_merge'].value_counts())
master_jp_im = master_jp_im.drop(columns=['_merge','FTA'])

# merge the tariff margin for each HS code for each EPA
master_jp_tariff = pd.read_pickle('../03_Output/jp_tariff_margin.pkl')
master_jp_im = master_jp_im.merge(master_jp_tariff,on=['TL','Duty Type/Code'],validate='m:1',how='left',indicator=True)
print(master_jp_im['_merge'].value_counts())

# left_only is not HS2022?, so drop it.
master_jp_im = master_jp_im[master_jp_im['_merge'] == 'both']

# filter out the HS codes that have Tariff Margin less than zero
master_jp_im = master_jp_im[master_jp_im['Tariff Margin'] > 0]
master_jp_im = master_jp_im.drop(columns=['_merge','Duty Type/Code','AV Duty Rate','Tariff Margin'])

# drop duplicates
master_jp_im = master_jp_im.drop_duplicates(keep='first',subset=['TL','Country'])

#%%
# export as pickle
master_jp_im.to_pickle('../03_Output/jp_tot_im.pkl')

# export as csv file
#master_jp_im.to_csv('../03_Output/jp_tot_im.csv')

