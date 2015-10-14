'''
Created on Oct 14, 2014

@author: adrian sarno


'''

import sys
import csv
import datetime
from sets import Set
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import pandas as pd
import numpy as np

def read_symbols_and_daterange(filename):
    symbols = Set()
    start_date = datetime.date(datetime.MAXYEAR, 1, 1)
    end_date = datetime.date(datetime.MINYEAR, 1, 1)
    
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    for row in reader:
        d = datetime.date(int(row[0]), int(row[1]), int(row[2]))
        if d < start_date:
            start_date = d
        elif d > end_date:
            end_date = d
        symbols.add(row[3])
    
    return list(symbols), start_date, end_date


def read_market_history(ls_symbols, dt_start, dt_end):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, datetime.timedelta(hours=16))
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    # adjusted close price
    vals = d_data["close"].values
    return pd.DataFrame(vals, index=ldt_timestamps, columns=ls_symbols)

def read_trade_matrix(ls_symbols, ldt_timestamps, filename):

    r = len(ldt_timestamps)
    c = len(ls_symbols)
    vals = np.zeros((r, c))
    # create dataframe
    df = pd.DataFrame(vals, index=ldt_timestamps, columns=ls_symbols )
    
    # now fill it up row by row
    reader = csv.reader(open(filename, 'rU'), delimiter=',')    
    for row in reader:
        # the date will be used a key (index) into the df
        d = datetime.datetime(int(row[0]), int(row[1]), int(row[2])) + datetime.timedelta(hours=16)
        # get the quantity 
        q = 0
        if row[4] == "Buy":
            q = int(row[5])
        elif row[4] == "Sell":
            q = -int(row[5])
        else:
            print "Unknown operation : (%s)" % (row[4]) 
        # get the symbol         
        s = row[3]       

        # Get the row corresponding to the date 
        v = np.array(df.ix[d])
        # update the column corresponding to the symbol
        v[ls_symbols.index(s)] += q 
        # place the updated row of values back in the matrix
        df.loc[d] = v
    
    return df


def create_cash_series(initial_cash, df_price, df_trade):

    v = np.zeros(len(df_trade.index))    
    ts_cash = pd.Series(v, index=df_trade.index)
    current_value = initial_cash
    
    for d in df_trade.index:       
        if not d in df_price.index:
            print "missing prices for %s" % (d)
        q = np.array(df_trade.ix[d])
        p = np.array(df_price.ix[d])
        current_value = current_value - sum(q * p)       
        ts_cash.ix[d] = current_value
    
    return ts_cash


def create_holding_series(df_price, df_trade):
    
    # use cumulative sum to convert trade matrix into holdings matrix
    df_holding = pd.DataFrame(np.cumsum(df_trade, axis=0), index=df_trade.index, columns=df_trade.columns)
    print df_holding
    
    # use dot product to calculate value of holdings in each date
    ts_holding = pd.Series(index=df_holding.index)
    for d in df_holding.index:       
        q = np.array(df_holding.ix[d])
        p = np.array(df_price.ix[d]) 
        ts_holding.ix[d] = np.dot(q, p)           
  
    return ts_holding


def main(argv):
    
    initial_cash = 1000000
    if len(argv) > 0 and (not argv[0] == None):
        initial_cash = int(argv[0])

    orders_file = "data/orders.csv"
    if len(argv) > 1 and (not argv[1] == None):
        orders_file = argv[1]

    values_file = "data/values.csv"
    if len(argv) > 2 and (not argv[2] == None):
        values_file = argv[2]
    
    
    # 1 - Read the dates and symbols
    (symbols, start_date, end_date) = read_symbols_and_daterange(orders_file)  
    print symbols, start_date, end_date 
    
    # 2 - Read the data
    df_price = read_market_history(symbols, start_date, end_date)  
    print df_price
    
    # 3 - Create the matrix of shares
    df_trade = read_trade_matrix(symbols, df_price.index, orders_file)  
    print df_trade
    
    # 4 - Calculate the cash timeseries
    ts_cash = create_cash_series(initial_cash, df_price, df_trade)
    print ts_cash
    
    # 5 - Calculate the holdings timeseries
    ts_holding = create_holding_series(df_price, df_trade)
    print ts_holding
    
    # 6 - Write to CSV
    writer = csv.writer(open(values_file, 'wb'), delimiter=',')
    for row_index in ts_holding.index:
        row_to_enter = [row_index, ts_holding[row_index] + ts_cash[row_index]]
        writer.writerow(row_to_enter) 
        print row_to_enter 

if __name__ == '__main__':
    main(sys.argv[1:])
        
    
    
    
    
    
    