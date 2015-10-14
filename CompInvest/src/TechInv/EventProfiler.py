'''

@author: Adrian Sarno

'''

import csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date

Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)

"""


def generate_trades(event_strategy, ls_symbols, df_events, s_file_name, i_trade_size, i_duration):
    event_strategy.orders_file = s_file_name + '.csv'
    writer = csv.writer(open(event_strategy.orders_file, 'wb'), delimiter=',') 
    #row_to_enter = ['Year', 'Month', 'Day', 'Symbol', 'Trade', 'Quantity']
    #writer.writerow(row_to_enter)
    ldt_timestamps = df_events.index
    last_day_index = len(ldt_timestamps)
    for i in range(1, last_day_index):
        for s_sym in ls_symbols:
            if df_events[s_sym].ix[ldt_timestamps[i]] == 1:
                dt_buy = ldt_timestamps[i]
                row_to_enter = [dt_buy.year, dt_buy.month, dt_buy.day, s_sym, 'Buy', i_trade_size]
                writer.writerow(row_to_enter)
                dt_sell = ldt_timestamps[last_day_index -1]               
                if (i + i_duration) < last_day_index:
                    dt_sell = ldt_timestamps[i + i_duration]
                row_to_enter = [dt_sell.year, dt_sell.month, dt_sell.day, s_sym, 'Sell', i_trade_size]
                writer.writerow(row_to_enter)

def profile_event(event_strategy, ls_symbols, dt_start, dt_end, df_events, i_trade_size, i_duration):
    s_file_name = 'work/%s_event_on_%s' % (event_strategy.getName(), event_strategy.s_list_name)
    lbd = event_strategy.i_lookback_days
    ep.eventprofiler(df_events, event_strategy.d_data, i_lookback=lbd, i_lookforward=lbd,\
                      s_filename=s_file_name + '.pdf', b_market_neutral=True, b_errorbars=True,\
                      s_market_sym=event_strategy.s_bench_sym)
    print "EventProfiler : %s study saved." % (s_file_name)   
    
    generate_trades(event_strategy, ls_symbols, df_events, s_file_name, i_trade_size, i_duration)

def profile_events(dt_start, dt_end, l_events):
    dataobj = da.DataAccess('Yahoo')

    for e in l_events:
        ls_symbols = dataobj.get_symbols_from_list(e.s_list_name)
        ls_symbols.append(e.s_bench_sym)     
        d_data = get_symbol_data(dataobj, ls_symbols, dt_start, dt_end)
        
        df_events, i_event_counter = e.find_events(ls_symbols, d_data)
        
        print "EventProfiler : For the %1.1f %s event with the components of %s, we find %d events. Date Range = (%s) to (%s)."\
        % (e.f_size, e.s_feature, e.s_list_name, i_event_counter, dt_start, dt_end)
            
        profile_event(e, ls_symbols, dt_start, dt_end, df_events, 100, 5)                    

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

    