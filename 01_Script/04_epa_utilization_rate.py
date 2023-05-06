# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:33:13 2023

@author: hayoshiz
"""

# import module
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# set defalut
plt.rcParams['figure.dpi'] = 300

# read pickle file
master_jp_epa = pd.read_pickle('../03_Output/jp_epa_im.pkl')
master_jp_im = pd.read_pickle('../03_Output/jp_tot_im.pkl')

#%%
## This section aims to calculate the EPA utilization rate in imports from country i for product p.
## Product p is in HS code section level. 

# initialize an empty dataframe
jp_epa_sum_bysection_bycountry = pd.DataFrame()
jp_im_sum_bysection_bycountry = pd.DataFrame()

# sum the import value by country name and HS codes
years = [str(year) for year in range(2012,2022)]
for year in years:
    jp_epa_sum_bysection_bycountry[year] = master_jp_epa.groupby(['Section','FTA Countries'])[year].sum()
    jp_im_sum_bysection_bycountry[year] = master_jp_im.groupby(['Section','FTA Countries'])[year].sum()
    
# calculate EPA utilization rate
ur_bysection_bycountry = jp_epa_sum_bysection_bycountry / jp_im_sum_bysection_bycountry

# export as csv file
ur_bysection_bycountry.to_csv('../03_Output/jp_ur_bysection_bycountry.csv')

#%%
## This section aims to calculate the EPA utilization rate in imports from country i.

# initialize an empty dataframe
jp_epa_sum_bycountry = pd.DataFrame()
jp_im_sum_bycountry = pd.DataFrame()

# sum the import value by country name and HS codes
for year in years:
    jp_epa_sum_bycountry[year] = master_jp_epa.groupby('FTA Countries')[year].sum()
    jp_im_sum_bycountry[year] = master_jp_im.groupby('FTA Countries')[year].sum()
    
# calculate EPA utilization rate
ur_bycountry = jp_epa_sum_bycountry / jp_im_sum_bycountry

# export as csv file
ur_bycountry.to_csv('../03_Output/jp_ur_bycountry.csv')

# extract 2021 data and sort from highest to lowest ur
ur_bycountry_2021 = ur_bycountry['2021'].sort_values(ascending=False)

# create figure
fig1,ax1 = plt.subplots()
ur_bycountry_2021.plot.barh(ax=ax1)
ax1.set_xlabel('FTA Utilization Rate')
ax1.set_ylabel("FTA Partner Country")
ax1.set_title("FTA Utilization Rate on Japan's Import in 2021")
fig1.tight_layout()

# export as png
fig1.savefig('../03_Output/jp_ur_bycountry_2021.png')



#%%
## This section aims to calculate the EPA utilization rate in imports for product p.
## Product p is in HS code section level. 

# initialize an empty dataframe
jp_epa_sum_bysection = pd.DataFrame()
jp_im_sum_bysection = pd.DataFrame()

# sum the import value by country name and HS codes
for year in years:
    jp_epa_sum_bysection[year] = master_jp_epa.groupby('Section')[year].sum()
    jp_im_sum_bysection[year] = master_jp_im.groupby('Section')[year].sum()
    
# calculate EPA utilization rate
ur_bysection = jp_epa_sum_bysection / jp_im_sum_bysection

# export as cev file
ur_bysection.to_csv('../03_Output/jp_ur_bysection.csv')

# extract 2021 data and sort from highest to lowest ur
ur_bysection_2021 = ur_bysection['2021'].sort_index(ascending=False)

# create figure
fig2,ax2 = plt.subplots()
ur_bysection_2021.plot.barh(ax=ax2)
ax2.set_xlabel('FTA Utilization Rate')
ax2.set_ylabel("Product")
ax2.set_title("FTA Utilization Rate on Japan's Import in 2021")
fig2.tight_layout()

# export as png
fig2.savefig('../03_Output/jp_ur_bysection_2021.png')

#%%
## This section aims to output pivot table of FTA utilization rate by product and by country.

ur_bysection_bycountry.reset_index(inplace=True)
ur_bysection_bycountry['2021'] = ur_bysection_bycountry['2021']*100
ur_bysection_bycountry['2021'] = round(ur_bysection_bycountry['2021'].astype(float),0)
table = ur_bysection_bycountry.pivot(index='Section', columns='FTA Countries', values='2021')

#%%
## This section is for testing. NOT FINALIZED.
## This section aims to calculate the EPA utilization rate. 

jp_im_sum = pd.DataFrame()

# sum the import value by year. 
jp_epa_sum = master_jp_epa[years]
jp_epa_sum = jp_epa_sum.sum()

# The sum for total import should differ since the difference in FTA affective year.
# 2012-2014
effective_fta = master_jp_im['FTA Countries'].isin(['ASEAN','Chile','India','Switzerland','Mexico','Peru'])
temp1 = master_jp_im[effective_fta == True]
temp1 = master_jp_im[[str(year) for year in range(2012,2015)]].sum()

# 2015
effective_fta = master_jp_im['FTA Countries'].isin(['Australia','ASEAN','Chile','India','Switzerland','Mexico','Peru'])
temp2_2015 = master_jp_im[effective_fta==True]
temp2_2015 = master_jp_im['2015'].sum()
print(temp2_2015)

# 2016-2018
effective_fta = master_jp_im['FTA Countries'].isin(['Australia','ASEAN','Chile','India','Switzerland','Mexico','Mongolia','Peru'])
temp3 = master_jp_im[effective_fta]
temp3 = master_jp_im[[str(year) for year in range(2016,2019)]].sum()

# 2019
effective_fta = master_jp_im['FTA Countries'].isin(['Australia','EU','ASEAN','Canada','Chile','India','New Zealand','Switzerland','United Kingdom','Mexico','Mongolia','Peru'])
temp4_2019 = master_jp_im[effective_fta]
temp4_2019 = master_jp_im['2019'].sum()
print(temp4_2019)

# 2020-2021
effective_fta = master_jp_im['FTA Countries'].isin(['Australia','EU','ASEAN','Canada','Chile','India','New Zealand','Switzerland','United Kingdom','United States of America','Mexico','Mongolia','Peru'])
temp5 = master_jp_im[effective_fta]
temp5 = master_jp_im[['2020','2021']].sum()

# concatnate all years
jp_im_sum = pd.concat([temp1,temp3,temp5])

###????
# export as cev file
#jp_im_sum.to_csv('../03_Output/for_cs_im.csv')
#temp2_2015.to_csv('../03_Output/for_cs_im2015.csv')
#temp4_2019.to_csv('../03_Output/for_cs_im2019.csv')
#jp_epa_sum.to_csv('../03_Output/for_cs_epa.csv')

# calculate EPA utilization rate
#ur = jp_epa_sum / jp_im_sum

# export as cev file
#ur.to_csv('../03_Output/jp_ur.csv')

