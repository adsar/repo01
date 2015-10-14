'''
Created on Oct 14, 2014

@author: adrian sarno


'''

import sys
import csv
import datetime
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import dateutil.parser as dp

def read_daterange(filename):

    ldt_timestamps = []
    
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    for row in reader:
        if len(row) > 0:
            d = dp.parse(row[0])
            ldt_timestamps.append(d)
        
    # sort ascending    
    ldt_timestamps.sort()   
    
    return ldt_timestamps[0], ldt_timestamps[len(ldt_timestamps) - 1]


def read_market_history(ls_symbols, dt_start, dt_end):
    dataobj = da.DataAccess('Yahoo')
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, datetime.timedelta(hours=16))
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    # adjusted close price
    vals = d_data["close"].values
    return pd.DataFrame(vals, index=ldt_timestamps, columns=ls_symbols)
     
       
def compute_stats(ts_daily_value):
    # Normalize the values to start at 1.0 and see 
    # the daily values relative to the initial value
    ts_norm_value = ts_daily_value / ts_daily_value[0]
    total_norm_return = ts_norm_value[len(ts_norm_value) - 1]
        
    # calculate the daily returns
    # ret(t) = (price(t)/price(t-1)) - 1
    # returnize works on numpy arrays and not in dataframes
    na_daily_return = ts_norm_value.values
    tsu.returnize0(na_daily_return)
        
    mean_rets = np.mean(na_daily_return)
    volatility = np.std(na_daily_return)
    
    # hardcode 252 instead of using actual year daycount to keep it comparable
    sharpe = math.sqrt(252) * mean_rets / volatility;

    return { 'avg_day_ret':mean_rets, 'volatility':volatility, 'sharpe':sharpe, 'total_return':total_norm_return, 'day_ret':na_daily_return}


def read_values(dt_start, dt_end, filename):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, datetime.timedelta(hours=16))
    r = len(ldt_timestamps)

    ts_values = pd.Series( np.zeros(r), index=ldt_timestamps)
    
    reader = csv.reader(open(filename, 'rU'), delimiter=',')    
    for row in reader:
        d = dp.parse(row[0])
        ts_values[d] = float(row[1])    
    
    return ts_values


def print_results(start, end, d_fund, d_ref, s_ref_symbol):
    print
    print ' Details of the Performance of the Portfolio :'
    print
    print ' Date Range : %s to %s' % (start, end)
    print
    print ' Sharpe Ratio of Fund : %s ' % (d_fund['sharpe'])
    print ' Sharpe Ratio of %s : %s ' % (s_ref_symbol, d_ref['sharpe'])
    print
    print ' Total Return of Fund : %s ' % (d_fund['total_return'])
    print ' Total Return of %s : %s ' % (s_ref_symbol, d_ref['total_return'])
    print
    print ' Standard Deviation of Fund : %s ' % (d_fund['volatility'])
    print ' Standard Deviation of %s : %s ' % (s_ref_symbol, d_ref['volatility'])
    print
    print ' Average Daily Return of Fund : %s ' % (d_fund['avg_day_ret'])
    print ' Average Daily Return of %s : %s ' % (s_ref_symbol, d_ref['avg_day_ret'])
    print 


def plot_results(ldt_timestamps, na_fund_day_ret, na_benchmark_day_ret, bechmark_symbol):
    plt.clf()

    # Calculate cumulative returns from daily returns
    na_fund_total = np.cumprod(na_fund_day_ret + 1)
    na_benchmark_total = np.cumprod(na_benchmark_day_ret + 1)

    # Plotting the results
    plt.clf()
    fig = plt.figure()
    fig.add_subplot(111)
    
    plt.plot(ldt_timestamps, na_benchmark_total, alpha=0.4)
    plt.plot(ldt_timestamps, na_fund_total)

    plt.legend([bechmark_symbol, 'Portfolio'])
    plt.ylabel('Cumulative Returns')
    
    fig.autofmt_xdate(rotation=30)
    plt.savefig("hw03Analizer.pdf", format="pdf")

    plt.show()
        
    
def main(argv):
    
    values_file = "data/values.csv"
    if len(argv) > 0 and (not argv[0] == None):
        values_file = argv[0]
    
    reference_symbol = "$SPX"
    if len(argv) > 1 and (not argv[1] == None):
        reference_symbol = argv[1]    

    # 1 - Read the dates
    (start_date, end_date) = read_daterange(values_file) 
    print start_date, end_date 
    
    # 2 - Read the data
    df_price = read_market_history([reference_symbol], start_date, end_date) 
    ts_ref_price = df_price[reference_symbol]
    
    print     
    print 'ts_ref_price'    
    print ts_ref_price    
    
    # 2 - Read the values timeseries
    ts_value = read_values(start_date, end_date, values_file)  
    print 
    print 'ts_value'
    print ts_value
            
    d_fund = compute_stats(ts_value)   
    d_ref = compute_stats(ts_ref_price)  
    
    print_results(start_date, end_date, d_fund, d_ref, reference_symbol) 
    
    plot_results(ts_value.index, d_fund["day_ret"], d_ref["day_ret"], reference_symbol)
    
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
        
    
    
    
    
    
    