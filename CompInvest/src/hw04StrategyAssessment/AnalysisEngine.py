'''
Created on Nov 01, 2014

@author: adrian sarno
'''

import sys
import datetime as dt

import EventStrategies as es
import EventProfiler as ep
import MarketSimulator as ms
import PerformanceAnalyst as pa

def main(argv):
    
    l_event_strategies = []

    l_event_strategies.append(es.UnderThreshold('sp5002012', 'actual_close', 9))
    #l_event_strategies.append(es.RelativeStrength('sp5002008', 'close', -5, 'SPY', 2))    
    #l_event_strategies.append(es.DailyChange('sp5002008', 'close', -10, '%'))
    #l_event_strategies.append(es.RelativeStrengthWithVolume('sp5002008', 'close', -5, 'SPY', 2))
    
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    
    print 'AnalysisEngine : Events to Analyze:'
    i = 0
    for e in l_event_strategies:
        i += 1
        print 'AnalysisEngine : %00d   - %s' % (i, e.getName())
        
    print
    print 'AnalysisEngine : Profiling Events'
    ep.profile_events(dt_start, dt_end, l_event_strategies)
    
    print
    print 'AnalysisEngine : Simulating Orders'
    ms.simulate_orders(50000, l_event_strategies)
    
    print
    print 'AnalysisEngine : Analyzing Results'
    pa.analize_results('$SPX', l_event_strategies, dt_start, dt_end)   

    
if __name__ == '__main__':
    main(sys.argv[0:])