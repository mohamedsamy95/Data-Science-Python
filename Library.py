# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 00:35:33 2020

@author: moham
"""
import pandas as pd
import datetime as dt

def exp_market_dataset(country, price_type = 'str' , date_format = '%m-%d-%Y'):
    dataset = pd.read_csv('Stock market data/' + country + ' Historical Data.csv' ,
                       dtype = {'Price' : price_type})
    if(isinstance(price_type,str)):
        dataset['Price'] = dataset['Price'].str.replace(',' , '')
        
    for i in range(dataset.shape[0]):
        dataset.loc[i, 'Date'] = dt.datetime.strptime(dataset.iloc[i]['Date'],
                                                      '%d-%b-%y').strftime(date_format)
    return dataset
    
def get_mean(dataset: pd.DataFrame, column, skipna = True):
    return dataset[column].mean(skipna)
    