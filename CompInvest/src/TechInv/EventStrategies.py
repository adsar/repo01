'''
Created on Oct 23, 2014

@author: adrian sarno
    
    The fundamental design tradeoff for the EventStrategies library is that you should be able
    to define absolutely all the detection, simulation and performance analysis parameters
    in a flexible way (meaning independently for each strategy) and then when you 
    process a batch of strategies, your engine should transparently take care of 
    processing time optimization by grouping together those strategies that use the same 
    datasets (e.g. sorting the batch by symbol collection and start and end time) 
    
'''
import TechnicalAnalysis as ta
import numpy as np
import copy

class Trade():
    '''
    classdocs
    '''
    def __init__(self, s_sym, f_quantity, dt_start, i_duration, f_expected_return):
       
        self.s_sym = s_sym
        
        self.f_quantity = f_quantity

        self.dt_start = dt_start

        self.i_duration = i_duration
        
        self.f_mean_expected_return = f_expected_return
        
class EventStrategy(object):
    '''
    classdocs
    '''
    def __init__(self, s_name, s_list_name, d_data, initial_cash):

        self.s_name = s_name
               
        self.s_list_name = s_list_name
        
        self.d_data = d_data
        
        self.initial_cash = initial_cash

        self.s_bench_sym = 'SPY'
       
        self.orders_file = ''
                
        self.l_trades = []
        
        self.i_transaction_count = 0

        self.f_sharpe = 0.0

    def getName(self):
        return "%s_%1.1f_%s" % (self.s_name, self.f_size, self.s_unit)
    
    def getValuesFile(self):
        return self.orders_file.replace('.csv', '_values.csv')
    
    def getAnalysisFile(self):
        return self.orders_file.replace('work/', 'out/').replace('.csv', '_performance.pdf')
    
    def getReportFile(self):
        return self.orders_file.replace('work/', 'out/').replace('.csv', '_perfom_summary.csv')
    
    def getOptimalTrade(self):
        return self.l_trades
    
        
class DailyChange(EventStrategy):
    '''
    classdocs
    '''
    def __init__(self, s_list_name, d_data):
        '''
        Constructor
        '''
        super(DailyChange, self).__init__('DailyChange', s_list_name, d_data)
            
    def find_events(self, ls_symbols, s_feature, f_size, s_unit):
        # Keep the size for generating appropriate names for output files
        self.ls_symbols = ls_symbols
        #the column of the data
        self.s_feature = s_feature            

        self.f_size = f_size 
        # Either $, %, etc
        self.s_unit = s_unit   
                       
        df_close = self.d_data[self.s_feature]
        i_event_counter = 0
           
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
                
                if self.s_unit == '%':
                    f_change = 100 * (f_symprice_yest - f_symprice_today)/f_symprice_yest
                else:
                    f_change = f_symprice_yest - f_symprice_today
                    
                if self.f_size >= 0:
                    if f_change >= self.f_size:
                        df_events[s_sym].ix[ldt_timestamps[i]] = 1
                        i_event_counter += 1
                else:
                    if f_change <= self.f_size:
                        df_events[s_sym].ix[ldt_timestamps[i]] = 1
                        i_event_counter += 1                       
    
        return df_events, i_event_counter

class BollingerRelWeakness(EventStrategy):
    '''
        Bollinger value for the equity today <= -2.0
        Bollinger value for the equity yesterday >= -2.0
        Bollinger value for SPY today >= 1.0
    '''
    def __init__(self, s_list_name, d_data, i_initial_cash, i_lookback_days):
        '''
        Constructor
        '''
        super(BollingerRelWeakness, self).__init__('BollingerRelWeakness', s_list_name, d_data, i_initial_cash)
        
        self.i_lookback_days = i_lookback_days

         
    def getName(self):
        return "%s_%1.1f_%s_vs_%s_%1.1f" % (self.s_name, self.i_lookback_days, self.f_size, self.s_bench_sym, self.f_bench_size)


    def find_events(self, ls_symbols, s_feature, f_size, s_bench_sym, f_bench_size):
        # Keep the args for generating appropriate names for output files
        self.ls_symbols = ls_symbols        
        #the column of the data
        self.s_feature = s_feature            
        self.f_size = f_size 
        self.s_bench_sym = s_bench_sym
        self.f_bench_size = f_bench_size   

           
        df_feature = self.d_data[self.s_feature]
        
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_feature)
        df_events = df_events * np.NAN
        i_event_counter = 0
            
        # Time stamps for the event range
        ts_study_range = df_feature.index

            
        ts_bench_price = df_feature[s_bench_sym]
        bbench = ta.TechnicalIndicator(s_bench_sym, ts_bench_price, self.i_lookback_days)
        dt_start = ts_study_range[0]
        dt_end = ts_study_range[len(ts_study_range) - 1]

        ts_bench_bollinger = bbench.getBollingerValue(dt_start, dt_end)
               
        for s_sym in ls_symbols:

            ts_price = df_feature[s_sym]
            bsym = ta.TechnicalIndicator(s_sym, ts_price, self.i_lookback_days)
            ts_sym_bollinger = bsym.getBollingerValue(dt_start, dt_end)
                   
            # The event profiler code will ignore the events near the beginning and near the end of the event array.  
            # The study code uses i_lookback=20 and i_lookforward=20 to specify how many days of info to remove.
            # Ignore the first 20 and last 20 days
            for i in range(self.i_lookback_days-1, len(ts_study_range)):
                # Calculating the change for this timestamp
                f_bollinger_today = ts_sym_bollinger[ts_study_range[i]]
                f_bollinger_yest = ts_sym_bollinger[ts_study_range[i - 1]]
                
                # calc benchmark 
                f_bench_bollinger_today = ts_bench_bollinger[ts_study_range[i]]

                if (f_bollinger_yest >= -self.f_size and f_bollinger_today < -self.f_size)\
                and f_bench_bollinger_today >= self.f_bench_size:
                    df_events[s_sym].ix[ts_study_range[i]] = 1
                    i_event_counter += 1                      
    
        return df_events, i_event_counter
