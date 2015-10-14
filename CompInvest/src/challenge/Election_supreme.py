'''
Created on Sep 29, 2014

@author: J.K.
'''
import sys
import csv
import random

from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


def read_data(file_path):
    data = []

    with open(file_path) as file:
        file.readline()

        for row in csv.reader(file):
            data.append((int(row[1]), float(row[2]) / 1.96))

    return data


def run_simulation(data):
    success = 0

    for params in data:
        if random.gauss(params[0], params[1]) > 0:
            success += 1

    return success


def print_results(results):
    print
    print '           Minimum: %s' % (np.amin(results))
    print '   25th Percentile: %s' % (np.percentile(results, 25))
    print '            Median: %s' % (np.median(results))
    print '   75th Percentile: %s' % (np.percentile(results, 75))
    print '           Maximum: %s' % (np.amax(results))
    print
    print '              Mean: %s' % (np.mean(results))
    print 'Standard Deviation: %s' % (np.std(results))
    print '          Variance: %s' % (np.var(results))
    print
    print 'Victory (discrete histogram, frequencies): %s' % (float(sum(i > 20 for i in results)) / len(results))
    print 'Victory (continuous normal, density) : %s' % (1 - norm(np.mean(results), np.std(results)).pdf(21))


def plot_results(results):
    plt.hist(results, bins = (np.amax(results) - np.amin(results)), normed = True)
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Probability')
    plt.show()
    
def plot_normal(results):
    x = np.linspace(0,36,360)
    plt.plot(x, mlab.normpdf(x, np.mean(results), np.std(results)))
    plt.title('Election Results')
    plt.xlabel('Margin')
    plt.ylabel('Density')
    plt.show()


def main(argv):
    data = read_data(argv[0])

    results   = []
    for _ in xrange(int(argv[1])):
        results.append(run_simulation(data))

    print_results(results)
    plot_results(results)
    plot_normal(results)


if __name__ == "__main__":
    main(sys.argv[1:])