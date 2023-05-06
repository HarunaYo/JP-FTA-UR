# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:33:13 2023

@author: hayoshiz
"""

# import module
import pandas as pd
import statsmodels.api as sm
import numpy as np

# read pickle file
master_jp_epa = pd.read_pickle('../03_Output/jp_epa_im.pkl')
master_jp_im = pd.read_pickle('../03_Output/jp_tot_im.pkl')

#%%
## This section aims to calculate the EPA utilization rate in imports from country i for poroduct p.
## Product p is in HS code 9 digit. 

# initialize an empty dataframe
jp_epa_sum_byhs9_bycountry = pd.DataFrame()
jp_im_sum_byhs9_bycountry = pd.DataFrame()

# sum the import value by country name and HS codes
years = [str(year) for year in range(2012,2022)]
for year in years:
    jp_epa_sum_byhs9_bycountry[year] = master_jp_epa.groupby(['TL','Country','Section'])[year].sum()
    jp_im_sum_byhs9_bycountry[year] = master_jp_im.groupby(['TL','Country','Section'])[year].sum()
   
# calculate EPA utilization rate
ur_byhs9_bycountry = jp_epa_sum_byhs9_bycountry / jp_im_sum_byhs9_bycountry

# convert the dataframe into a long list
ur_byhs9_bycountry = ur_byhs9_bycountry.stack()

# reset index
ur_byhs9_bycountry = ur_byhs9_bycountry.reset_index(drop=False)

# rename the column
ur_byhs9_bycountry = ur_byhs9_bycountry.rename(columns={'level_3':'Year',0:'UR'})

#%%
## This section aims to calculate the monthly EPA imports.

# initialize an empty dataframe
monthly_im = pd.DataFrame()

# create monthly import data
for year in years:
    # sum the annual imports by country per HS code because some countries have several EPAs and the import data is seperated.
    monthly_im[year] = master_jp_epa.groupby(['TL','Country','Section'])[year].sum()
    # convert the annual data into monthly import
    monthly_im[year] = monthly_im[year] / 12

# convert the dataframe into a long list
monthly_im = monthly_im.stack()

# reset index
monthly_im = monthly_im.reset_index(drop=False)

# rename the column
monthly_im = monthly_im.rename(columns={'level_3':'Year',0:'Monthly IM'})


#%%
## This section aims to calculate the average tariff margin per country per product.
## We need to do this because some countries have several EPAs.

# create average tariff margin data by country per HS code because some countries have several EPAs and the import data is seperated.
ave_tariff_margin = master_jp_epa.groupby(['TL','Country','Section'])['Tariff Margin'].mean()

# reset index
ave_tariff_margin = ave_tariff_margin.reset_index(drop=False)

# rename the column
ave_tariff_margin = ave_tariff_margin.rename(columns={'Tariff Margin':'Ave Tariff Margin'})

#ave_tariff_margin.to_csv('../03_Output/ave_tariff_margin.csv')

#%%
## This section aims to conduct a regression analysis on EPA utilization rate.
## EPA utilization rate = monthy imports + tariff margin + year_dummy

# merge all the variables into one dataframe
merge = ur_byhs9_bycountry.merge(monthly_im,on=['TL','Country','Year','Section'],how='left',validate='1:1',indicator=True)
print(merge['_merge'].value_counts())
merge = merge.drop(columns=['_merge'])
merge = merge.merge(ave_tariff_margin,on=['TL','Country','Section'],how='left',validate='m:1',indicator=True)
print(merge['_merge'].value_counts())
merge = merge.drop(columns=['_merge'])

# get log for 'Monthly IM'
merge['ln_Monthly IM'] = merge['Monthly IM'].apply(np.log)

# replace -inf with 0
merge['ln_Monthly IM'] = merge['ln_Monthly IM'].replace(-np.inf,0)

# create dummies
#dummy_country = pd.get_dummies(merge['Country'])
#dummy_section = pd.get_dummies(merge['Section'])
#dummy_year = pd.get_dummies(merge['Year'])

#merge = merge.join([dummy_country,dummy_section,dummy_year])

# set variables
ind_var = sm.add_constant(merge[['ln_Monthly IM','Ave Tariff Margin']])
dep_var = merge['UR']

# conduct linear regression using OLS method
model = sm.OLS(dep_var,ind_var)

# result
result = model.fit()

# print and export the summary as text
summary = result.summary().as_text()
print(summary)
with open(f'../03_Output/jp_regression_summary.txt','w') as f:
    f.write(summary)

# extract and print key elements of the result
#est = result.params
#cov = result.cov_params()
#print('Extracted parameter estimates:\n',est)
#print('Extracted parameter convariance matrix:\n',cov)
