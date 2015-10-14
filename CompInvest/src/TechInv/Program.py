'''
Created on Oct 23, 2014

@author: adrian sarno
'''

import sys
import datetime as dt

import EventStrategies as es
import EventProfiler as ep
import MarketSimulator as ms
import PerformanceAnalyst as pa
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du

def get_symbol_data(dataobj, ls_symbols, dt_start, dt_end):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    ls_keys = ['close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    
    return d_data

def main(argv):
    
    # parameters
    s_list_name = 'sp5002012'
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    s_bench_sym = 'SPY'
    i_initial_cash = 100000    

    print 'TechInv : Bollinger Event Study'
    
    # read market data
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(s_list_name)
    ls_symbols.append(s_bench_sym)     
    d_data = get_symbol_data(dataobj, ls_symbols, dt_start, dt_end)
    
    # create the object that implements the strategy   
    event_strategy = es.BollingerRelWeakness(s_list_name, d_data, i_initial_cash, 20)
    df_events, i_event_counter = event_strategy.find_events(ls_symbols, 'close', 2.0, s_bench_sym, 1.3)
        
    print "EventProfiler : For the %1.1f %s event with the components of %s, we find %d events. Date Range = (%s) to (%s)."\
    % (event_strategy.f_size, event_strategy.s_feature, event_strategy.s_list_name, i_event_counter, dt_start, dt_end)
        
    print 'TechInv : Profiling Events'
    ep.profile_event(event_strategy, ls_symbols, dt_start, dt_end, df_events, 100, 5)
    

    print ''
    ms.simulate_market(event_strategy)
              
    event_strategy.s_bench_sym = '$SPX'
    print ''
    pa.analyze_event(event_strategy, dt_start, dt_end)
    
if __name__ == '__main__':
    main(sys.argv[0:])