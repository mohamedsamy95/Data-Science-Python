# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 00:35:33 2020

@author: moham
"""
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

def exp_market_dataset(country, price_type = 'str' , date_format = '%m-%d-%Y'):
    dataset = pd.read_csv('Stock market data/' + country + ' Historical Data.csv' ,
                       dtype = {'Price' : price_type})
    if(isinstance(price_type,str)):
        dataset['Price'] = dataset['Price'].str.replace(',' , '')
        
    for i in range(dataset.shape[0]):
        dataset.loc[i, 'Date'] = dt.datetime.strptime(dataset.iloc[i]['Date'],
                                                      '%d-%b-%y').strftime(date_format)
    return dataset


def plot_and_save(death_rates: pd.DataFrame , countries, 
                  yaxis, xaxis = 'Day' , save_datasets = False):
    
    #Initialize canvas
    sns.set_context('notebook')
    sns.set_style('darkgrid')
    sns.set(font_scale=1.5)
    
    #Create figure object
    fig = plt.figure(figsize=(40,15))
    fig.subplots_adjust(hspace=0.5, wspace=0.4)
    plot = 1
    
    #Load stock market data for each country
    for country in countries:
        stock_data = exp_market_dataset(country, date_format = '%#m/%#d/%Y')
        
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
        if(save_datasets):
            death_stock_rates.to_csv('Factor results/' + country + ' factor.csv')
            
        #Reset index and convert data type to float for plotting and regression calculations
        death_stock_rates = death_stock_rates.T.reset_index()
        death_stock_rates['Market value'] = death_stock_rates['Market value'].astype(float)
        death_stock_rates['Death'] = death_stock_rates['Death'].astype(float)
        death_stock_rates['Ratio'] = death_stock_rates['Ratio'].astype(float)
        
        #Initialize a 3x7 figure 
        plt.subplot(3,7,plot)
        
        #Day 1,2,3,.. instead of dates
        if xaxis == 'Day':
            days = list(range(1, death_stock_rates.shape[0]+1))
            ax = sns.regplot(x= days , y= yaxis, data= death_stock_rates)
            plt.xlabel(xaxis)
        else:
            ax = sns.regplot(x= xaxis , y= yaxis, data= death_stock_rates)
            xticks = ax.get_xticks()
            plt.xticks([xticks[0] , xticks[-1]] , visible=True )
            plt.xlabel(xaxis + ' rate %')
        if yaxis == 'Market value':
            plt.ylabel('Index change %')
        elif yaxis == 'Death':
            plt.ylabel('Death rate %')
        else:
            plt.ylabel(yaxis)
        
        ax.set_title(country)
        
        
        #Save figure
        plt.savefig('Factor results/' + yaxis + ' vs ' + xaxis)
        plot += 1
    