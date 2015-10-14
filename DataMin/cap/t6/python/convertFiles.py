import json
from pprint import pprint
import io
import random
import json
import csv

#path2filesIn="/mnt/hgfs/sh_dev/Hygiene/"
path2filesIn="../../../../Dropbox/files/DataMin/cap/data/t6/Hygiene/"
path2review=path2filesIn+"hygiene.dat"
path2feature=path2filesIn+"hygiene.dat.additional"
path2label=path2filesIn+"hygiene.dat.labels"

#path2filesOut="/mnt/hgfs/sh_dev/Dropbox/files/DataMin/cap/data/t6/data/"
path2filesOut="../../../../Dropbox/files/DataMin/cap/data/t6/data/"

def main():
    toJson()
    toCsv()

def toCsv():
    outExtension=".csv"
    path2reviewOut=path2filesOut+"hygiene"+outExtension
    path2featureOut=path2filesOut+"hygiene.additional"+outExtension
    path2labelOut=path2filesOut+"hygiene.labels"+outExtension
    c = 0
    with open(path2reviewOut, "wb+") as fo:
        fo.write("review\r\n")
        with open (path2review, 'r') as f:
            for line in f.readlines():
                c = c + 1
                doc = line[:-1].translate(None, '\t\n\r')
                l = min(len(doc), 20000)
                fo.write("{}\r\n".format(doc[0:l]))
    print 'reviews: ', c

    c = 0
    with open(path2labelOut, "wb+") as fo:
        fo.write("label\r\n")
        with open (path2label, 'r') as f:
            for line in f.readlines():
                c = c + 1
                fo.write("{}\r\n".format(line[:-1]))
    print 'labels: ', c

    c = 0
    with open(path2featureOut, "wb+") as fo:
        fo.write("cuisines,zipcode,review-count,rating\r\n")
        with open (path2feature, 'r') as f:
            for line in f.readlines():
                c = c + 1
                fo.write("{}\r\n".format(line[:-1]))
    print 'feature rows: ', c

def toJson():
    outExtension=".json"
    path2reviewOut=path2filesOut+"hygiene"+outExtension
    path2featureOut=path2filesOut+"hygiene.additional"+outExtension
    path2labelOut=path2filesOut+"hygiene.labels"+outExtension

    with open(path2reviewOut, "wb+") as fo:
        with open (path2review, 'r') as f:
            for line in f.readlines():
                review = {'review': line[:-1]}
                js = json.dumps(review)
                fo.write("{}\r\n".format(js))

    with open(path2labelOut, "wb+") as fo:
        with open (path2label, 'r') as f:
            for line in f.readlines():
                label = {'label': line[:-1]}
                js = json.dumps(label)
                fo.write("{}\r\n".format(js))

    with open(path2featureOut, "wb+") as fo:
        with open (path2feature, 'r') as f:
            for line in f.readlines():
                for fields in csv.reader([line[:-1]], skipinitialspace=True):
                    feature = {'cuisines': fields[0], 'zipcode': int(fields[1]), 'review-count': int(fields[2]), 'rating': float(fields[3])}
                    js = json.dumps(feature)
                    fo.write("{}\r\n".format(js))

if __name__=="__main__":    
    main()
