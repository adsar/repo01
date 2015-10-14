'''

@author: Adrian Sarno

'''
import sys
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import TechnicalAnalysis as ta
import pandas as pd

def create_indicators(ls_symbols, dt_start, dt_end, i_lookback):
    d_indicators = {}
    
    dataobj = da.DataAccess('Yahoo')
    d_data = get_symbol_data(dataobj, ls_symbols, dt_start, dt_end)
    df_close = d_data['close']
    for sym in ls_symbols:
        ts_price = df_close[sym]
        b = ta.TechnicalIndicator(sym, ts_price, 20)
        d_indicators[sym] = b
        
    return d_indicators       

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
    
    ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']   

    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    i_lookback = 20
    f_width = 2
    inds = create_indicators(ls_symbols, dt_start, dt_end, i_lookback)

    dt_s = dt.datetime(2010, 6, 1)
    dt_e = dt.datetime(2010, 12, 30)
    
    df_bollinger_value = pd.DataFrame()   

    for s in ls_symbols:
        ts_bollinger_value = inds[s].getBollingerValue(dt_s, dt_e)     
        df_bollinger_value[s] = ts_bollinger_value     
        print   
        print
        print "Bollinger Signal of %s, for trade strategy" % inds[s].s_symbol
        ts_price = inds[s].getPriceSeries(dt_s, dt_e)          
        ts_bol_signal = inds[s].getBollingerSignal(dt_s, dt_e, f_width)
        df_signal = pd.concat([ts_price, ts_bollinger_value, ts_bol_signal], axis=1)
        print df_signal
        print
        print "Bollinger Bands for Plotting"        
        df_bands =  inds[s].getBollingerBands(dt_s, dt_e, f_width)
        print df_signal[[s]].join(df_bands)
        inds[s].plot_bollinger(dt_s, dt_e, f_width)
    
    print
    print df_bollinger_value
    
if __name__ == '__main__':
    main(sys.argv[0:])