# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:15:26 2020

@author: moham
"""

import pandas as pd
import numpy as np
import datetime as dt
import Library as l

#Sample of countries we are dealing with
countries = ['Austria', 'Canada', 'China', 'Czech Republic', 'Denmark', 'Ecuador', 'France', 
             'Germany', 'Ireland', 'Israel', 'Italy', 'Netherlands', 'Portugal',
             'Romania', 'Serbia', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
             'United Kingdom', 'United States']

#Read data into dataframes
population_data = pd.read_csv('Corona datasets/Population_by_country_2020.csv', 
                                  dtype = {'Population (2020)' : 'float'})
population_data = population_data.set_index('Country (or dependency)')

death_data = pd.read_csv('Corona datasets/time_series_covid19_deaths_global.csv')
death_data = death_data.set_index('Country/Region')

#Create new dataframe to hold death rates and remove unneccessary columns 
death_rates = pd.DataFrame(columns = death_data.columns)
death_rates = death_rates.drop(['Province/State', 'Lat', 'Long'] , axis=1)
death_rates ['Country/Region'] = pd.Series(countries)
death_rates = death_rates.set_index('Country/Region')

#Loop through our list of countries
for country in countries: 
    #create a list of dataframe columns
    columns = list(death_rates)
    #iterating through all dates
    for i in columns:
        death_cases = death_data.loc[country][i]
        #Handling the case of multiple entries for same country
        if (not isinstance(death_cases, int)): 
            death_cases = death_cases.sum()
        
        population = population_data.loc[country]['Population (2020)']
        death_percent = (death_cases / population) * 100
        #Add value into cell
        death_rates.loc[country,i] = death_percent
  
death_rates.to_csv('Corona datasets/death_rates.csv')

#Load stock market data for each country
for country in countries:
    stock_data = l.exp_market_dataset(country, date_format = '%#m/%#d/%Y')
    
    #Change shape of dataframe to match death_rates
    stock_data = stock_data.T
    stock_data.columns = stock_data.loc['Date']
    stock_data = stock_data.drop(['Date'], axis =0)
    stock_data = stock_data.drop(['Price', 'Open', 'High', 'Low', 'Vol.'], axis=0)
    
    #Create new dataframe that holds both death rates and percent price change for a country
    death_stock_rates = pd.DataFrame(columns = stock_data.columns)
    death_stock_rates = death_stock_rates.rename(columns={'Date' : 'Rates'})
    death_stock_rates['Rates'] = pd.Series(['Market value', 'Death', 'Ratio'])
    death_stock_rates = death_stock_rates.set_index('Rates')

    #create a list of dataframe columns
    columns = list(death_stock_rates)

    #iterating through all dates
    for i in columns:
        #Add values to cells
        change = float(stock_data.loc['Change %'][i].replace('%' , ''))
        death_stock_rates.loc['Market value',i] = change
        death = death_rates.loc[country][i]
        death_stock_rates.loc['Death',i] = death
        if death !=0 :
            death_stock_rates.loc['Ratio',i] = round(change/death , 2)
    
    #Save table into csv file
    death_stock_rates.to_csv('Factor results/' + country + ' factor.csv')
            
    
