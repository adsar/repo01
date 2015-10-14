'''
In order to win the senate, the Republicans will have to win 21 of the 36 races
this November. 
What is the probability they will win 21 of these races?



Created on Sep 28, 2014

@author: adrian
'''



# QSTK Imports

# Third Party Imports
import pandas as pd
import numpy as np
import random as rn
from scipy.stats import norm 
import matplotlib.pyplot as plt

print "Pandas Version", pd.__version__
print "NumPy Version", np.__version__


def plot_results(results):
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = True)
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Probability')
    plt.show()

def main():
    ''' Main Function'''
    # Reading the poll results
    na_senate = np.loadtxt('senate.csv', dtype='S20,f4, f4',
                        delimiter=',', comments="#", skiprows=1)
    print na_senate

    # Sorting the poll results by state
    na_senate = sorted(na_senate, key=lambda x: x[0])
    print na_senate

    # Create lists for each race: 
    # race name, republican advantage, margin of error
    ls_race_name = []
    lf_rep_margin = []
    lf_err = []
    for race_poll in na_senate:
        ls_race_name.append(race_poll[0])
        lf_rep_margin.append(race_poll[1])
        lf_err.append(race_poll[2])
        

    # simulate the election a large number of times
    # and count how many times the total of republican victories in the
    # simulated races has reached or surpassed the required number of victories
    # to win majority in the senate
    n = 10000
    i_rep_sen = 0
    i_req_number = 21
    li_sim_result = []
    for rep in range(n):     
        # init a counter to tally total republican victories in the simulated election
        i_rep_vic = 0
        for s_race_name in ls_race_name:
            i_index = ls_race_name.index(s_race_name)
            f_rep_adv = lf_rep_margin[i_index]
            f_err = lf_err[i_index]
            if rn.gauss(f_rep_adv, f_err/1.96) > 0.0:
                i_rep_vic += 1
       
        # debug
        print "repetition = ", rep, "   --   victories = ", i_rep_vic
        print ""
        
        # store result for each repetition of the simulation
        li_sim_result.append(i_rep_vic)
        
        # count if republican achieved majority in senate
        if i_rep_vic >= i_req_number:
            i_rep_sen += 1
    
    # estimate the parameters of distribution of the simulation results
    x = np.array(li_sim_result)
    f_mu = x.mean()
    f_sigma = x.std()
    print "mu=", f_mu, "  --  sigma=", f_sigma
    
    # print the result
    f_prob = 1 - norm(f_mu, f_sigma).pdf(i_req_number)
    print "Probability of republicans winning the senate = ", f_prob  
    
    plot_results(li_sim_result)



if __name__ == '__main__':
    main()

