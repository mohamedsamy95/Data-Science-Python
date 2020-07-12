# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:37:47 2020

@author: Mohamed Elsisi
"""

import pandas as pd
import numpy as np
import datetime as dt
import Library as l
import matplotlib.pyplot as plt
import seaborn as sns


countries = ['Austria', 'Canada', 'China', 'Czech Republic', 'Denmark', 'Ecuador', 'France', 
             'Germany', 'Ireland', 'Israel', 'Italy', 'Netherlands', 'Portugal',
             'Romania', 'Serbia', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
             'United Kingdom', 'United States']

df = pd.DataFrame(columns = ['Country', 'Start Price', 'End Price', 'Change %','Death Cases', 'Population(2020)', 'Death %',
                             'Factor'])


for country in countries:
    stock_data = l.exp_market_dataset(country, date_format = '%#m/%#d/%Y')
    population_data = pd.read_csv('Corona datasets/Population_by_country_2020.csv', 
                                  dtype = {'Population (2020)' : 'float'})
    population_data = population_data.set_index('Country (or dependency)')
    death_data = pd.read_csv('Corona datasets/time_series_covid19_deaths_global.csv')
    death_data = death_data.set_index('Country/Region')
    
    start_price = stock_data.iloc[0]['Price']
    end_price = stock_data.iloc[-1]['Price']
    change_percent = ((float(end_price) - float(start_price)) / float(start_price)) * 100
    
    death_cases = death_data.loc[country][stock_data.iloc[-1]['Date'] ]
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

#df.to_csv('Factor results/death_stock_rates.csv')

#Initialize canvas
sns.set_context('notebook')
sns.set_style('darkgrid')
sns.set(font_scale=1.5)
    
#Create figure object
fig, ax = plt.subplots(figsize = (40,15))
rect = ax.bar(list(df['Country']), list(df['Factor']), 
              color = ['red', 'blue', 'black', 'yellow', 'cyan', 'green', 'orange'] )

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if height > 0:
            v = 'bottom'
        else:
            v = 'top'
        ax.text(rect.get_x() + rect.get_width()/2., 1.03*height,'%d' % int(height),
                ha='center', va=v)

autolabel(rect)        
plt.xticks(rotation = 90)
plt.savefig('Factor results/Summary')
