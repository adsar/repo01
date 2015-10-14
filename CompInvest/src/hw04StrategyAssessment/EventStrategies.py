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
    def __init__(self, s_name, s_list_name, s_feature, f_size, s_unit, initial_cash):

        self.s_name = s_name
               
        self.s_list_name = s_list_name
        
        #the column of the data
        self.s_feature = s_feature
        #the amount of change (with sign)
        self.f_size = f_size
        # % or $
        self.s_unit = s_unit

        self.s_bench_sym = 'SPY'
       
        self.orders_file = ''
                
        self.l_trades = []
        
        self.i_transaction_count = 0

        self.initial_cash = initial_cash

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
    def __init__(self, s_list_name, s_feature, f_size, s_unit):
        '''
        Constructor
        '''
        super(DailyChange, self).__init__('DailyChange', s_list_name, s_feature, f_size, s_unit, 0)
            
    def find_events(self, ls_symbols, d_data):
        ''' Finding the event dataframe '''
        df_close = d_data[self.s_feature]
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


class RelativeStrength(EventStrategy):
    '''
    classdocs
    '''
    def __init__(self, s_list_name, s_feature, f_percent, s_bench_sym, f_bench_percent):
        '''
        Constructor
        '''
        super(RelativeStrength, self).__init__('RelativeStrength', s_list_name, s_feature, f_percent, '%', 0)
                
        # benchmark symbol to compare
        self.s_bench_sym = s_bench_sym
        #the % of change in benchmark  (with sign)
        self.f_bench_size = f_bench_percent
         
    def getName(self):
        return "%s_%1.1f_%s_vs_%s_%1.1f" % (self.s_name, self.f_size, self.s_unit, self.s_bench_sym, self.f_bench_size)
    
    def comp(self, f_change, f_percent):
        if f_percent >= 0:
            if f_change >= f_percent:
                return True
        elif f_change <= f_percent:
            return True
        return False

    def find_events(self, ls_symbols, d_data):
        ''' Finding the event dataframe '''
        df_close = d_data[self.s_feature]
        ts_bench = df_close[self.s_bench_sym]
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
                
                # calc benchmark movement
                f_bench_symprice_today = ts_bench[ldt_timestamps[i]]
                f_bench_symprice_yest = ts_bench[ldt_timestamps[i - 1]]
                
                
                f_change = 100 * (f_symprice_today/f_symprice_yest - 1)
                f_bench_change = 100 * (f_bench_symprice_today/f_bench_symprice_yest - 1)

                    
                if self.comp(f_change, self.f_size) and self.comp(f_bench_change, self.f_bench_size):
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1
                    i_event_counter += 1                      
    
        return df_events, i_event_counter


class RelativeStrengthWithVolume(EventStrategy):
    '''
    classdocs
    '''
    def __init__(self, s_list_name, s_feature, f_percent, s_bench_sym, f_bench_percent):
        '''
        Constructor
        '''
        super(RelativeStrengthWithVolume, self).__init__('RelativeStrengthWithVolume', s_list_name, s_feature, f_percent, '%', 0)
        
        # benchmark symbol to compare
        self.s_bench_sym = s_bench_sym
        #the % of change in benchmark  (with sign)
        self.f_bench_size = f_bench_percent
                 
    def getName(self):
        return "%s_%1.1f_%s_vs_%s_%1.1f" % (self.s_name, self.f_size, self.s_unit, self.s_bench_sym, self.f_bench_size)

    def comp(self, f_change, f_percent):
        if f_percent >= 0:
            if f_change >= f_percent:
                return True
        elif f_change <= f_percent:
            return True
        return False

    def find_events(self, ls_symbols, d_data):
        ''' Finding the event dataframe '''
        df_close = d_data[self.s_feature]
        df_volume = d_data['volume']
        ts_bench_volume = df_volume[self.s_bench_sym]
        ts_bench_close = df_close[self.s_bench_sym]
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
                f_symvolume_today = df_volume[s_sym].ix[ldt_timestamps[i]]
                f_symvolume_yest = df_volume[s_sym].ix[ldt_timestamps[i - 1]]
                
                # calc benchmark movement
                f_bench_symprice_today = ts_bench_close[ldt_timestamps[i]]
                f_bench_symprice_yest = ts_bench_close[ldt_timestamps[i - 1]]
                f_bench_symvolume_today = ts_bench_volume[ldt_timestamps[i]]
                f_bench_symvolume_yest = ts_bench_volume[ldt_timestamps[i - 1]]
                
                
                f_change = 100 * (f_symprice_today/f_symprice_yest - 1)
                f_bench_change = 100 * (f_bench_symprice_today/f_bench_symprice_yest - 1)
                f_change_volume = 100 * (f_symvolume_today/f_symvolume_yest - 1)
                f_bench_change_volume = 100 * (f_bench_symvolume_today/f_bench_symvolume_yest - 1)

                    
                if self.comp(f_change, self.f_size) and self.comp(f_bench_change, self.f_bench_size):
                    if self.comp(f_change_volume, 20) and self.comp(f_bench_change_volume, -10):
                        df_events[s_sym].ix[ldt_timestamps[i]] = 1
                        i_event_counter += 1                      
    
        return df_events, i_event_counter


class UnderThreshold(EventStrategy):
    '''
    classdocs
    '''
    def __init__(self, s_list_name, s_feature, f_size):
        '''
        Constructor
        '''
        super(UnderThreshold, self).__init__('UnderThreshold', s_list_name, s_feature, f_size, '$', 0)

    
    def find_events(self, ls_symbols, d_data):
        ''' Finding the event dataframe '''
        df_close = d_data[self.s_feature]
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
            for i in range(0, len(ldt_timestamps)):
                # Calculating the returns for this timestamp
                f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
                f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
                               
                if f_symprice_yest >= self.f_size and f_symprice_today < self.f_size:
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1
                    i_event_counter += 1                       
    
        return df_events, i_event_counter

