# -*- coding: utf-8 -*-
"""
Author:     Derron Stein
e-mail:     derron.stein@du.edu
Version:    1.0
Code Purpose:
Imports a stock purchase data from csv file
Imports stock open and close values from a json file
saves stock data to a database file
displays stock plot graph
functions located in db.py, financial_assets.py, and Stock_Data_yahoo.py
required modules:  yfinance, tdqm, pandas, sqlite3, datetime, matplotlib, csv, os, and json

Code Inputs:
imports stock data from Lesson6_Data_Stocks.csv
import stocks from yahoo from date purchased until the current date
if yahoo data is not available imports static stock data from AllSTocks.json
Code Output:
simplePlot.png
mydatabase.db
"""
from datetime import datetime
import matplotlib.pyplot as plt
import os
import csv
from financial_assets import is_int, validate_header, is_date
from db import create_table, insert_table
from Stock_Data_Yahoo import load_yahoo_stocks
from pandas.plotting import register_matplotlib_converters
import pandas as pd
from tqdm import tqdm

register_matplotlib_converters()

db = 'myDatabase.db'
data_file = 'AllStocks.json'
stock_file = 'Lesson6_Data_Stocks.csv'
stock_header = ['SYMBOL', 'NO_SHARES', 'PURCHASE_PRICE', 'CURRENT_VALUE', 'PURCHASE_DATE']
stock_price = []

#load stock purchase price list
if  os.path.exists(stock_file):
    try:
        with open(stock_file) as csvfile:
            reader = csv.DictReader(csvfile) 
            is_valid_csv = validate_header (stock_header, list(reader.fieldnames))

            if is_valid_csv:
                for line in reader:
                    if len(line['SYMBOL']) > 0 and is_int(line['NO_SHARES'] and 
                    is_date(line['PURCHASE_DATE'])):
                        try:
                            stock_price.append({'Symbol': line['SYMBOL'],  
                                        'Shares': int(line['NO_SHARES']),
                                        'Date': datetime.strptime(line['PURCHASE_DATE'], '%m/%d/%Y'),
                                        'End_Date': datetime.now()})
                        except:
                            print("Invalid data on row")
                            print(line)
                    else:
                        print("Invalid data on row")
                        print(line)
    except:
        print(f"Invalid file content:  {stock_file}")
else:
    print(f'File not found:  {stock_file}')
    exit


#Retrieve stock purchase price list items from yahoo repository
print ('Downloading stock data from the web')
data, successful_download = load_yahoo_stocks(stock_price)

if not successful_download:
    #load stocks from json file
    if not os.path.exists(data_file):
        print(f'Cannot find {data_file}')
        exit

    try:
        # returns JSON object as a dictionary
        print('Could not download data from the web')
        print('Loading sample data')
        data = pd.read_json(data_file)
        data = data.set_index('Date')
        
    except:
        print('Jason data could not be loaded')
        exit

#load data into database
if (create_table(db)):
    insert_table(db, data)

#Load data into chart from data
count = 0
for stock in stock_price:
    x = []
    y = []
    with tqdm(total=len(data), desc=f"Loading {stock['Symbol']} stock graph data", unit='Records') as pbar:
        for ind, row in data.iterrows():
            if row['Symbol'] == stock['Symbol']:
                try:
                    x.append(ind)
                    y.append(stock['Shares'] * row['Close'])
                except:
                    pass
            pbar.update()
                
    plt.plot(x, y, label = stock['Symbol'])


# show a legend on the plot
plt.legend()
# save plot
plt.savefig('simplePlot.png')
# function to show the plot
plt.show()

