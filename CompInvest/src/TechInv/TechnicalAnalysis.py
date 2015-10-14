'''
Created on Oct 29, 2014

@author: adrian
'''
import pandas as pd
import matplotlib.pyplot as plt

class TechnicalIndicator(object):
    '''
    This class does not read the market data, the caller 
    that reads the market data and passes it as a time series.
    This class calculates and stores the rolling mean and rolling std
    '''


    def __init__(self, s_symbol, ts_price, i_lookback_days):
        '''
        Constructor
        '''
        self.s_symbol = s_symbol
        self.i_lookback_days = i_lookback_days
        
        self.s_std_col = 'rolling_std_%s' % (self.i_lookback_days)
        self.s_mean_col = 'rolling_mean_%s' % (self.i_lookback_days)    
 
        #self.df_data = pd.DataFrame(ts_price.resample("1D", fill_method="ffill"), columns=[s_symbol])
        self.df_data = pd.DataFrame(ts_price, columns=[s_symbol])
         
    def calc(self):      
        ts_std = pd.rolling_std(self.df_data[self.s_symbol], window=self.i_lookback_days, min_periods=self.i_lookback_days/2)
        self.df_data[self.s_std_col] = ts_std

        ts_mean = pd.rolling_mean(self.df_data[self.s_symbol], window=self.i_lookback_days, min_periods=self.i_lookback_days/2)
        self.df_data[self.s_mean_col] = ts_mean
        
    def getPriceSeries(self, dt_s, dt_e):  
        return self.df_data[self.s_symbol][dt_s:dt_e]
                 
    def getMeanSeries(self, dt_s, dt_e): 
        if self.s_mean_col not in self.df_data.columns:
            self.calc() 
        return self.df_data[self.s_mean_col][dt_s:dt_e]
          
    def getStdSeries(self, dt_s, dt_e): 
        if self.s_std_col not in self.df_data.columns:
            self.calc() 
        return self.df_data[self.s_std_col][dt_s:dt_e]
              
    # for event
    def getBollingerValue(self, dt_s, dt_e): 
        if self.s_std_col not in self.df_data.columns:
            self.calc() 
        
        fun_boll_value =  lambda row: (row[0] - row[1]) / row[2]
 
        ts_bol_val = (self.df_data[[self.s_symbol, self.s_mean_col, self.s_std_col]][dt_s:dt_e]).apply(fun_boll_value, axis=1)
        ts_bol_val.name = "BollingerValue"
        
        return ts_bol_val
    
    def getBollingerSignal(self, dt_s, dt_e, f_width): 
        
        fun_signal = lambda x: "oversold" if x <= -1 else ("overbought" if x >= 1 else "neutral") 
        
        ts_signal = (self.getBollingerValue(dt_s, dt_e) / f_width).apply(fun_signal)
        ts_signal.name = "Signal"
        
        return ts_signal 
     
    # for plotting   
    def getBollingerBands(self, dt_s, dt_e, f_width): 
        if self.s_std_col not in self.df_data.columns:
            self.calc()            

        lbb = self.df_data[self.s_mean_col][dt_s:dt_e] - f_width * self.df_data[self.s_std_col][dt_s:dt_e]
        hbb = self.df_data[self.s_mean_col][dt_s:dt_e] + f_width * self.df_data[self.s_std_col][dt_s:dt_e]
        
        df = pd.concat([lbb, self.df_data[self.s_mean_col][dt_s:dt_e], hbb], axis=1)
        df.columns = ['lbb', 'mean', 'hbb']
        
        return df
    

    def plot_trade_windows(self, dt_s, dt_e, f_width):
        ts_signal = self.getBollingerValue(dt_s, dt_e)
        dt_previous = ''
        s_color_previous = ''
        
        for i in range(len(ts_signal)):
            # get values for the current date
            dt = ts_signal.index[i]
            s = ts_signal[dt]
            s_color = 'r' if s >= f_width else 'g' if s <= -f_width else ''
                            
            # update the figure: on change and in last day
            if s_color != s_color_previous \
            or (i == len(ts_signal)-1):
                
                # if we are ending a trade opportunity window
                if s_color_previous != '':
                    # shade the trade opportunity window
                    plt.axvspan(dt_previous, dt, color=s_color_previous, alpha=0.25)
                    
                    # draw the end line
                    plt.axvline(x=dt, color=s_color_previous, alpha=0.5)
                
                # if we are starting a new trade opportunity window
                if s_color != '':
                    # draw the start line
                    plt.axvline(x=dt, color=s_color, alpha=0.5)
                
                # save the last event
                s_color_previous = s_color
                dt_previous = dt


    def plot_bollinger(self, dt_s, dt_e, f_width):
        plt.clf()
        
        ldt_timestamps = self.df_data[self.s_symbol][dt_s:dt_e].index   
    
        fig = plt.figure(1)
        plt.subplots_adjust(hspace=0.5)      
        
        # Plot the Bands
        fig.add_subplot(211)  
        plt.title('%s Bollinger Bands' % (self.s_symbol))
        s_label = 'rolling mean (%d)' % (self.i_lookback_days)
        df_bands =  self.getBollingerBands(dt_s, dt_e, f_width)
        plt.plot(ldt_timestamps, df_bands['mean'], 'k--', label=s_label, alpha=1.0)
        plt.fill_between(ldt_timestamps, df_bands['lbb'], df_bands['hbb'], color='black', alpha=0.25, linestyle='dashed')
        
        ts_price = self.getPriceSeries(dt_s, dt_e)
        plt.plot(ldt_timestamps, ts_price, 'b-', label='adj.close')              
                        
        plt.legend(loc='upper right')
        plt.ylabel('Price')
        
        maxy = 1.05 * df_bands['hbb'].max()
        miny = 0.90 * df_bands['lbb'].min()
        plt.ylim(ymin=miny, ymax=maxy)
        
        fig.autofmt_xdate(rotation=30)
        
        self.plot_trade_windows(dt_s, dt_e, f_width)
             
        # Plot the Signal
        fig.add_subplot(212)         
        plt.title('%s Signal' % (self.s_symbol))
        miny = -f_width
        maxy = f_width
        plt.ylim(ymin=2 * miny, ymax=2 * maxy)
        plt.fill_between(ldt_timestamps, miny, maxy, color='black', alpha=0.25, linestyle='dashed')

        plt.plot(ldt_timestamps, self.getBollingerValue(dt_s, dt_e), 'b-', alpha=1.0, label='Bollinger Value')
        plt.legend(loc='upper right')
        plt.ylabel('Normalized Price')        
        fig.autofmt_xdate(rotation=30)
        
        self.plot_trade_windows(dt_s, dt_e, f_width)     
                        
        #Output                
        name = '%s_bollinger_%d' % (self.s_symbol, self.i_lookback_days)
        plt.savefig(name, format="pdf")
        print "TechnicalIndicator : %s saved." % (name)
    
        plt.show()
        
        