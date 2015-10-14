'''

@author: Adrian Sarno

'''



import numpy as np
import copy
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
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_PriceDrop_events(ls_symbols, d_data, f_price_drop):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    i_event_counter = 0
       
    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        # The event profiler code will ignore the events near the beginning and near the end of the event array.  
        # The study code uses i_lookback=20 and i_lookforward=20 to specify how many days of info to remove.
        # Ignore the first 20 and last 20 days
        for i in range(20, len(ldt_timestamps) - 20):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
    
            # Event is found if the symbol is price went from above $5 yesterday
            # to under $5 today
            if f_symprice_yest >= f_price_drop and f_symprice_today < f_price_drop:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                i_event_counter += 1
                

    return df_events, i_event_counter

def generate_study_for_events(dataobj, ls_symbols, dt_start, dt, dt_end, s_year, f_price_drop):
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events, i_event_counter = find_PriceDrop_events(ls_symbols, d_data, f_price_drop)
    
    print "For the $%1.1f event with the components of the S&P500 in %s, we find %d events. Date Range = (%s) to (%s)." % (f_price_drop, s_year, i_event_counter, dt_start, dt_end)
    
    s_file_name = 'hw02EventStudy_%s_%1.1f.pdf' % (s_year, f_price_drop)

    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename=s_file_name, b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
    print "Study saved: ", s_file_name
    return

def scan_for_event(spx_year, f_price_drop):
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp500' + spx_year)
    ls_symbols.append('SPY')   
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)   
    generate_study_for_events(dataobj, ls_symbols, dt_start, dt, dt_end, spx_year, f_price_drop)
    return

if __name__ == '__main__':
    scan_for_event('2012', 5.0)
    scan_for_event('2008', 5.0)
    #scan_for_event('2008', 7.0)
    #scan_for_event('2012', 9.0)

