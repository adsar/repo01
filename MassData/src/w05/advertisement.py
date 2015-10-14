'''
Created on Nov 10, 2014

@author: adrian
'''
import pandas as pd
import numpy as np


def init_advert():
    df = pd.DataFrame(index=['A', 'B', 'C', 'D', 'E'])
    df["Bid"] = pd.Series([.1, .09, .08, .07, .06], index=df.index)
    df["CTR1"] = pd.Series([.015, .016, .017, .018, .019], index=df.index)
    df["CTR2"] = pd.Series([.010, .012, .014, .015, .016], index=df.index)
    df["CTR3"] = pd.Series([.005, .006, .007, .008, .010], index=df.index)
    df["Budget"] = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=df.index)
    df["Assigned"] = pd.Series(['', '', '', '', ''], index=df.index)
    df["TotalCT"] = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0], index=df.index)
    
    return df


def assign_slots(df):
    advertisers = []
    df["Assigned"] = pd.Series(['', '', '', '', ''], index=df.index)
    for slot in ['CTR1', 'CTR2', 'CTR3']:
        maxw = 0
        imaxw = -1
        for index, row in df[(df['Budget'] > 0) & (df['Assigned'] == '')].iterrows():
            weight = row['Bid'] * row[slot]
            if weight > maxw:
                maxw = weight
                imaxw = index
        if imaxw >= 0:
            df['Assigned'].ix[imaxw] = slot
            advertisers.append(imaxw)
    
    return advertisers


def publish_slots(df, advertisers):
    budget = True
    while sum(df["TotalCT"]) < 101 and budget:
        for index in advertisers:
            slot = df['Assigned'].ix[index]
            if df['Budget'].ix[index] > 0:
                df['Budget'].ix[index] -= df['Bid'].ix[index] * df[slot].ix[index]
                df["TotalCT"].ix[index] += df[slot].ix[index]
            else:
                budget = False
        print df

def main():
    df = init_advert()
    print df
    
    while sum(df["TotalCT"]) < 101:
        advertisers = assign_slots(df)
        print advertisers
        publish_slots(df, advertisers)
        print df
    
if __name__ == '__main__':
    main()