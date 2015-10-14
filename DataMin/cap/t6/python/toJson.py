import json
from pprint import pprint
import io
import random
import json
import csv

path2filesIn="/mnt/hgfs/sh_dev/Hygiene/"
path2review=path2filesIn+"hygiene.dat"
path2feature=path2filesIn+"hygiene.dat.additional"
path2label=path2filesIn+"hygiene.dat.labels"

path2filesOut="/mnt/hgfs/sh_dev/Dropbox/files/DataMin/cap/data/t6/data/"
#path2filesOut="/mnt/hgfs/sh_dev/Hygiene/"
path2reviewjson=path2filesOut+"hygiene.json"
path2featurejson=path2filesOut+"hygiene.additional.json"
path2labeljson=path2filesOut+"hygiene.labels.json"


with open(path2reviewjson, "wb+") as fo:
    with open (path2review, 'r') as f:
        for line in f.readlines():
            review = {'review': line[:-1]}
            js = json.dumps(review)
            fo.write("{}\n".format(js))

with open(path2labeljson, "wb+") as fo:
    with open (path2label, 'r') as f:
        for line in f.readlines():
            label = {'label': line[:-1]}
            js = json.dumps(label)
            fo.write("{}\n".format(js))

with open(path2featurejson, "wb+") as fo:
    with open (path2feature, 'r') as f:
        for line in f.readlines():
            for fields in csv.reader([line[:-1]], skipinitialspace=True):
                feature = {'restaurant': {'cuisines': fields[0], 'zipcode': int(fields[1]), 'review-count': int(fields[2]), 'rating': float(fields[3])}}
                js = json.dumps(feature)
                fo.write("{}\n".format(js))





