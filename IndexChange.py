# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:37:47 2020

@author: Mohamed Elsisi
"""

import pandas as pd
import numpy as np
import datetime as dt

countries = ['Austria', 'Canada', 'China', 'Czech Republic', 'Denmark', 'Ecuador', 'France', 
             'Germany', 'Ireland', 'Israel', 'Italy', 'Netherlands', 'Portugal',
             'Romania', 'Serbia', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
             'United Kingdom', 'United States']

df = pd.DataFrame(columns = ['Country', 'Start Price', 'End Price', 'Change %','Death Cases', 'Population(2020)', 'Death %',
                             'Factor'])


for (country,i) in zip( countries,range(len(countries)) ):
    stock_data = pd.read_csv('Stock market data/' + country + ' Historical Data.csv' ,
                       dtype = {'Price' : 'str'})
    population_data = pd.read_csv('Population_by_country_2020.csv', 
                                  dtype = {'Population (2020)' : 'float'})
    population_data = population_data.set_index('Country (or dependency)')
    death_data = pd.read_csv('Corona datasets/time_series_covid19_deaths_global.csv')
    death_data = death_data.set_index('Country/Region')
    
    start_price = stock_data.iloc[-1]['Price'].replace(',' , '')
    end_price = stock_data.iloc[0]['Price'].replace(',' , '')      
    change_percent = ((float(end_price) - float(start_price)) / float(start_price)) * 100
    
    death_cases = death_data.loc[country][dt.datetime.strptime(stock_data.iloc[0]['Date'], 
                                                               '%b %d, %Y').strftime('%#m/%#d/%Y')]
    if (not isinstance(death_cases, int)):
        death_cases = death_cases.sum()
        
    population = population_data.loc[country]['Population (2020)']
        
    death_percent = (death_cases / population) * 100
    
    row = {'Country' : country, 'Start Price' : round(float(start_price) , 2), 
           'End Price' : round(float(end_price) , 2), 'Change %' : round(change_percent, 2),
           'Death Cases' : death_cases,
           'Population(2020)' : population,
           'Death %' : death_percent , 
           'Factor' : round(change_percent / death_percent) }
    df = df.append(row , ignore_index = True)
    
print(df)

df.to_csv('death_stock_rates.csv')

