'''
Created on Oct 16, 2014

@author: adrian
'''

import sys
import datetime
import time
import pandas as pd
from pandas.io.data import DataReader


def getMarketData(symbols, beginDate, endDate, symbolsSkipped):
    symbolsSkipped = []
    d_price = {}
    
    for symbol in symbols:
        try:
            reader = DataReader(symbol,"yahoo", beginDate, endDate) 
            priceSeries = reader['Adj Close']
            d_price[symbol] = priceSeries
        except:
            symbolsSkipped.append(symbol)
            
    return pd.DataFrame(d_price)


def main(argv):
    
    beginDate = datetime.date(2014, 1, 1)
    endDate = datetime.date.today() + datetime.timedelta(hours=16)
    symbols = ['AAPL', 'GOOG', 'INTC', 'MSFT', 'RIG', 'QCOM', 'MO', 'PM', 'TVIX']    
    skipped = []
    
    df_price = getMarketData(symbols, beginDate, endDate, skipped)

    print df_price
    print skipped

    

if __name__ == '__main__':
    main(sys.argv[1:])