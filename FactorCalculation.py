# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:15:26 2020

@author: moham
"""

import pandas as pd
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

#Plots with different variables, save factor datasets only once
l.plot_and_save(yaxis = 'Market value', death_rates = death_rates, countries = countries,
                #save_datasets = True)
l.plot_and_save(yaxis = 'Death', death_rates = death_rates, countries = countries)
l.plot_and_save(yaxis = 'Ratio', death_rates = death_rates, countries = countries)

l.plot_and_save(xaxis = 'Death', yaxis = 'Market value', 
                death_rates = death_rates, countries = countries)



    
            
    
