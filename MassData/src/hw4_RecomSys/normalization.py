'''
Created on Oct 20, 2014

@author: adrian
'''
import numpy as np
import pandas as pd

def question01():
    movie = ['M', 'N', 'P', 'Q', 'R']
    user = ['A', 'B', 'C']
    value = np.array([1, 2, 3, 4, 5, 2, 3, 2, 5, 3, 5, 5, 5, 3, 2])
    value = value.reshape(len(user), len(movie))
    value = value.astype(float)
    df_rating = pd.DataFrame(value, index=user, columns=movie)
    print df_rating
    
    # normalize rows
    for i in range(len(user)):
        avg = np.mean(df_rating.ix[user[i]])
        for j in range(len(movie)):
            v = df_rating.ix[user[i]][movie[j]]
            v = v - avg
            df_rating.set_value(user[i], movie[j], v)

    print
    print 'Normalized rows'
    print df_rating    
    # check
    a = np.array(df_rating)
    print
    print 'Row totals:'
    # sum over all the columns (axis 1)
    row_tot = a.sum(axis=1).reshape((3,1))
    print np.round(row_tot, 2)
    
    # normalize each column
    movie_mean = np.array(a.mean(axis=0))
    a = a - movie_mean[None, :]
    df_rating = pd.DataFrame(a, index=user, columns=movie)
    print
    print 'Normalized columns:'
    print df_rating
    
    # check
    print
    print 'Column Totals:'
    col_tot = a.sum(axis=0)
    print np.round(col_tot, 2)
    # check
    a = np.array(df_rating)
    print
    print 'Row totals:'
    # sum over all the columns (axis 1)
    row_tot = a.sum(axis=1).reshape((3,1))
    print np.round(row_tot, 2)
        
    # find min
    print
    a = np.array(df_rating)
    minval = a.min()
    maxval = a.max()
    for u in df_rating.index:
        for m in df_rating.columns:
            if df_rating.ix[u][m] == minval:
                print 'min is [%s, %s]' % (u, m)
            if df_rating.ix[u][m] == maxval:
                print 'max is [%s, %s]' % (u, m)

def main():
    question01()

if __name__ == '__main__':
    main()