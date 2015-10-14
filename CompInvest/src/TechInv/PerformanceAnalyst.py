'''
Created on Oct 14, 2014

@author: adrian sarno


'''

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

    initial_value = ts_daily_value.head(1)
    final_value = ts_daily_value.tail(1)
    
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

    return { 'avg_day_ret':mean_rets, 'volatility':volatility, 'sharpe':sharpe,\
             'total_return':total_norm_return, 'day_ret':na_daily_return,\
             'initial_value':initial_value, 'final_value':final_value}


def read_values(dt_start, dt_end, filename):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, datetime.timedelta(hours=16))
    r = len(ldt_timestamps)

    ts_values = pd.Series( np.zeros(r), index=ldt_timestamps)
    
    reader = csv.reader(open(filename, 'rU'), delimiter=',')    
    for row in reader:
        d = dp.parse(row[0])
        ts_values[d] = float(row[1])    
    
    return ts_values


def save_report(start, end, d_fund, d_ref, s_ref_symbol, portfolio_name, trade_count):
       
    writer = csv.writer(open(portfolio_name, 'wb'), delimiter=',')
    
    row_to_enter = ['Details of the Performance of the Portfolio : ', portfolio_name]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Date Range : ', '%s to %s' % (start, end)]
    writer.writerow(row_to_enter)  
    
    row_to_enter = ['Transactions : ', '%d' % (trade_count)]  
    writer.writerow(row_to_enter) 
    
    row_to_enter = ['Sharpe Ratio of Fund : ', '%s ' % (d_fund['sharpe'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Sharpe Ratio of %s : ' % (s_ref_symbol), '%s' % (d_ref['sharpe'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Total Return of Fund : ', '%s' % (d_fund['total_return'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Total Return of %s : ' % (s_ref_symbol), '%s' % (d_ref['total_return'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Standard Deviation of Fund : ', '%s' % (d_fund['volatility'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Standard Deviation of %s : ' % (s_ref_symbol), '%s' % (d_ref['volatility'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Average Daily Return of Fund : ', '%s' % (d_fund['avg_day_ret'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Average Daily Return of %s : ' % (s_ref_symbol), '%s' % (d_ref['avg_day_ret'])]
    writer.writerow(row_to_enter)    

    row_to_enter = ['Initial Value of Fund : ', '%d' % (d_fund['initial_value'])]
    writer.writerow(row_to_enter) 

    row_to_enter = ['Final Value of Fund : ', '%d' % (d_fund['final_value'])]
    writer.writerow(row_to_enter) 
            
    print "PerformanceAnalyst : %s report saved." % (portfolio_name)


def print_results(start, end, d_fund, d_ref, s_ref_symbol, protfolio_name, trade_count):
    print 
    print 'PerformanceAnalyst : Details of the Performance of the Portfolio : %s' % (protfolio_name)
    print 'PerformanceAnalyst : Date Range : %s to %s' % (start, end)
    print 'PerformanceAnalyst : Transactions : %d' % (trade_count)
    print
    print 'PerformanceAnalyst : Sharpe Ratio of Fund : %s ' % (d_fund['sharpe'])
    print 'PerformanceAnalyst : Sharpe Ratio of %s : %s ' % (s_ref_symbol, d_ref['sharpe'])
    print
    print 'PerformanceAnalyst : Total Return of Fund : %s ' % (d_fund['total_return'])
    print 'PerformanceAnalyst : Total Return of %s : %s ' % (s_ref_symbol, d_ref['total_return'])
    print
    print 'PerformanceAnalyst : Standard Deviation of Fund : %s ' % (d_fund['volatility'])
    print 'PerformanceAnalyst : Standard Deviation of %s : %s ' % (s_ref_symbol, d_ref['volatility'])
    print
    print 'PerformanceAnalyst : Average Daily Return of Fund : %s ' % (d_fund['avg_day_ret'])
    print 'PerformanceAnalyst : Average Daily Return of %s : %s ' % (s_ref_symbol, d_ref['avg_day_ret'])
    print 
    print 'PerformanceAnalyst : Initial Value of Fund : %d' % (d_fund['initial_value'])
    print 'PerformanceAnalyst : Final Value of Fund : %d' % (d_fund['final_value'])
    print 


def plot_results(ldt_timestamps, na_fund_day_ret, na_benchmark_day_ret, bechmark_symbol, plot_name):
    plt.clf()

    # Calculate cumulative returns from daily returns
    na_fund_total = np.cumprod(na_fund_day_ret + 1)
    na_benchmark_total = np.cumprod(na_benchmark_day_ret + 1)

    # Plotting the results
    fig = plt.figure()
    fig.add_subplot(111)
    
    plt.plot(ldt_timestamps, na_benchmark_total, alpha=0.4)
    plt.plot(ldt_timestamps, na_fund_total)

    plt.legend([bechmark_symbol, 'Portfolio'])
    plt.ylabel('Cumulative Returns')
    
    fig.autofmt_xdate(rotation=30)
    plt.savefig(plot_name, format="pdf")
    print "PerformanceAnalyst : %s report saved." % (plot_name)

    #plt.show()
 
 

def analyze_event(es, start_date, end_date):
    # 1 - Read the dates
    (start_date, end_date) = read_daterange(es.getValuesFile())
    
    # 2 - Read the data
    df_price = read_market_history([es.s_bench_sym], start_date, end_date)
    ts_ref_price = df_price[es.s_bench_sym]
#print
#print 'ts_ref_price'
#print ts_ref_price
# 3 - Read the values timeseries
    ts_value = read_values(start_date, end_date, es.getValuesFile())
#print
#print 'ts_value'
#print ts_value
# 4 - Compute stats
    d_fund = compute_stats(ts_value)
    d_ref = compute_stats(ts_ref_price)
# 5 - write output
    save_report(start_date, end_date, d_fund, d_ref, es.s_bench_sym, es.getReportFile(), es.i_transaction_count)
    print_results(start_date, end_date, d_fund, d_ref, es.s_bench_sym, es.getName(), es.i_transaction_count)
    plot_results(ts_value.index, d_fund["day_ret"], d_ref["day_ret"], es.s_bench_sym, es.getAnalysisFile())

def analize_results(benchmark_symbol, l_event_strategies, start_date, end_date):
    for es in l_event_strategies:
        es.s_bench_sym = benchmark_symbol
 
        analyze_event(es, start_date, end_date)
