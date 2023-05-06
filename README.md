# Observation of Japan's FTA Utilization Rate

## Purpose of the Analysis
In an international trade, firms may benefit through utilizing Free Trade Agreement (FTA) by reducing their tariff burdens. However, there are also costs associated such as learning cost of rules of origin and certification procedures for each FTA, Certification costs to customs etc..
Therefore, if costs exceed benefits, there is a high possibility that FTA will not be utilized.
The purpose of the project is to analyze  Japan's FTA utilization rate on imports and explore its determinants through regression analysis. For the determinants, the Tariff Margin and the Monthly Import is used. 

## Datasets
+ **Japan's total import data**"\n"
Source: [Japan Custom](https://www.customs.go.jp/toukei/info/)
    - CIF import value
    - national tariff line level (HS (Harmonized System) nine-digit level)
    - annual data of 2012 to 2021
    - HS2017 version

+ **Japan's FTA utilized import data**
Source: [Japan Custom](https://www.customs.go.jp/kyotsu/kokusai/toukei/)
    - CIF import value
    - national tariff line level (HS nine-digit level)
    - annual data of 2012 to 2021
    - data for 2012 to 2016: HS2012 version\n
      data for 2016 to 2021: HS2017 version

+ **Japan's MFN tariff rate and FTA tariff rate**
Source: [World Trade Organization](https://tao.wto.org/welcome.aspx?ReturnUrl=%2f)
    - national tariff line level (HS nine-digit level)
    - HS2017 version

*Note*: As of May 2023, Japan has concluded 20 RTAs with 50 countries in force. However, the latest FTA, RCEP (Regional Comprehensive EPA), which was concluded in January 2022 will not be included in the analysis since the annual import data was only available until 2021. 

## Regression Model
The specific regression model used in this project is as follows. *FTA Utilization Rate* is the dependant variable and *Tariff Margin* and *Monthly Imports* are the independant variables. 


*FTA Utilization Rate* = α*Tariff Margin* + βln*Monthly Imports*



Definition of the variables:
- *FTA Utilization Rate*: the FTA utilization rates in imports from country i for product p in year t. Product is defined at national tariff line which is the most detailed data we can get from trade data. 
As explained before, FTA utilization rate is defined as the share of imports of  products that are eligible under to receive such preferential tariff rates. 
0% indicates FTA is not being utilized and 100% indicates FTA is at perfect utilization. 

- *Tariff Margin*: the absolute difference between FTA tariff rate and MFN tariff rate on product p from country i in year t.
As explained above, products with zero tariff margin, which are ineligible to receive preferential tariff rate, is not included. 
It shall be noted that simplification is made regarding to the calculation of tariff margin. Some countries like Australia, Brunei, Chile, Indonesia, Malaysia, Mexico, Peru, Philippines, Singapore, Thailand and Vietnam have sevral FTAs concluded with Japan. Since tariff margin may differ for each FTA, I defined the tariff margin as the average tariff margin of all FTAs. Although firms may intuitively chose to use the FTA with the largest tariff margin, there may be other factors that effect their decision. To this end, I decided to use the average instead of using the maximum tariff margin of all FTAs option.

- *Monthly Imports*: the average of monthly imports of products p from country i in year t. This variable is suppose to define as a firm-level transaction sizes. Due to data availability, this was the nearest estimation that can be made for firm-level transaction size. 

## Explanation of the Scripts

1. '01_tariffmargin.py'

1. '02_epa_imports.py'

1. '03_total_imports.py'

1. '04_epa_utilization_rate.py'

1. '05_regression_analysis.py'

## Regression Results
![alt text](C:\Users\hayoshiz\OneDrive - Syracuse University\Capstone Project\JP-FTA-UR\03_Output/regression_summary.csv "????")


Above is the result of the regression model estimated by the simple ordinary least squares (OLS) method. 

The result shows that the regression model has a good overall fit as indicated by the high R-squared value of 0.692.

Coefficient for both *Tariff Margin* and *Monthly Imports* shows positive relation with the *FTA Utilization Rate*. This result is reasonable in a common sense that as the tariff margin become larger, it implies the gain from applying FTA tariff rate will increase, which leads to greater incentive to use FTA for firm. Also, similarly, as the transaction size is bigger for the firm, incentive to use FTA will be greater.

## Conclusion
Based on the regression analysis, I have two options to improve FTA utilization rate: to increase tariff margin or to increase the size of the import. However, since import size depends on the decision of the importer (the firms), it is not realistic for the government to intervene to change firm's decision making. Likewise, as tariff is needed to protect the domestic industry, it is not ideal to lower the FTA tariff rate to increase the tariff margin.

In hence, policies to promoting positive factors (tariff margin and import size) are limited. 
It is assumed that the negative factors are the main obstacle for utilizing FTA as seen from the past research papers.

Therefore, for future research should include negative factors such as *restrictiveness of rules of origin* and other *various costs* as independent variables in the regression model.
