'''
Created on Oct 01, 2014

@author: A.S.
'''
import sys

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import math

def read_data(ls_symbols, dt_start, dt_end):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, in a 3-dimensional Panda dataframe.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    # now d_data is a dictionary
    # for each of the keys there is a matrix with
    # one row for each Timestamp and one column for each symbol.    
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    # Getting the matrix for the 'close' prices,
    # as a numpy array.
    na_price = d_data['close'].values  
    return na_price

    
# Returns all legal allocations for the list of symbols
# legal means sum = 1.00, with variations of .10
def get_legal_allocations(moneyAvailable, symbolsToBuy, allocation, allocations):
    # if there are symbols to allocate and haven't used more that 100% of investment capital
    if symbolsToBuy and moneyAvailable >= 0:
        for amount in xrange(0, moneyAvailable + 1, 10):
            allocation.append(float(amount))
            get_legal_allocations(moneyAvailable - amount, symbolsToBuy[1:], allocation, allocations)            
            allocation.pop()
    else:
        if (not symbolsToBuy) and moneyAvailable == 0:
            allocations.append(np.array(allocation) / 100)

    return


def simulate_fund_performance(start, end, symbols, allocation):
    # read the close price for the symbols and period of choice
    na_price = read_data(symbols, start, end)
    
    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    
    # normalized daily returns for each symbol
    # ret(t) = (price(t)/price(t-1)) -1
    na_daily_rets = na_normalized_price.copy()
    tsu.returnize0(na_daily_rets)
       
    # Calculate daily normalized price of the fund
    # 1. Assign an amount proportional to the initial allocation 
    #    in the first row (start date), as if total fund value was $1
    # 2. Apply the normalized daily returns compounding in each successive date
    #    to calculate the cumulative returns of each symbol proportional to initial 
    #    allocation:  daily_cum_ret(t) = daily_cum_ret(t-1) * (1 + daily_ret(t))
    # 3. For each row, calculate the total value in an added column
    #    note this is the value that an initial $1 fund would have each day.
    # 4. Copy the column containing the fund total in a separate array
    dayCount = na_daily_rets.shape[0]
    symbolCount = na_daily_rets.shape[1]
    na_positions_daily_value = np.zeros([dayCount, symbolCount + 1])
    na_positions_daily_value[0,:] = np.append(allocation[:], 1.0)
    for t in range(1, dayCount):
        na_positions_daily_value[t, 0:symbolCount] = na_positions_daily_value[t-1, 0:symbolCount] * (1 + na_daily_rets[t, :])
        na_positions_daily_value[t, symbolCount] = sum(na_positions_daily_value[t, 0:symbolCount])

    # normalized daily returns for fund
    # ret(t) = (price(t)/price(t-1)) -1
    na_fund_daily_rets = na_positions_daily_value[:,symbolCount].copy()
    tsu.returnize0(na_fund_daily_rets)  
      
    # calculate fund stats
    fund_mean_rets = np.mean(na_fund_daily_rets)
    fund_volatility = np.std(na_fund_daily_rets)
    
    # hardcoded 252 instead of using dayCount to match course wiki
    fund_sharpe = math.sqrt(252) * fund_mean_rets / fund_volatility;
    fund_cum_return = na_positions_daily_value[dayCount-1, symbolCount]

    return (fund_mean_rets, fund_volatility, fund_sharpe, fund_cum_return)

def print_results(start, end, ls_symbols, allocation, results):
    print
    print '                  Start / end dates: %s' % ([start.strftime('%c'), end.strftime('%c')])
    print '                            Symbols: %s' % (ls_symbols)
    print '                 Optimal allocation: %s' % (allocation)
    print
    print '            Fund Mean Daily Returns: %s' % (results[0])
    print 'Volatility (stdev of daily returns): %s' % (results[1])
    print '                  Fund sharpe ratio: %s' % (results[2])
    print '             Fund cumulative return: %s' % (results[3])
    print    
    print '             Fund cumulative return: %%%.2f' % (100 * (results[3] - 1))
    print

def main(argv):

    # Arguments
    ls_symbols = ['BRCM', 'ADBE', 'AMD', 'ADI']  
    year = 2010
   
    # get all the possible legal Allocations for a $ 100 fund
    legalAllocations = []
    get_legal_allocations(100, ls_symbols, [], legalAllocations)
    
    # start and end date of the year to analyze
    start = dt.datetime(year, 1, 1)
    end = dt.datetime(year, 12, 31)
    
    # select the allocation that optimizes the sharpe ratio
    maxAllocation = legalAllocations[0]
    maxResults = simulate_fund_performance(start, end, ls_symbols, maxAllocation)
    for allocation in legalAllocations[1:]:
        results = simulate_fund_performance(start, end, ls_symbols, allocation)
        if results[2] > maxResults[2]:
            maxResults = results
            maxAllocation = allocation 

    print_results(start, end, ls_symbols, maxAllocation, maxResults)


if __name__ == "__main__":
    main(sys.argv[1:])