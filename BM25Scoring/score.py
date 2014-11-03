#!/usr/bin/env python

import sys
import re
import os
import math

idfpath = 'data/idf.dat'
tfpath = 'data/tfcount.dat'
wordcountpath = 'data/wordcount.dat'
inputdir = '../Presidents'


splice = lambda x: x.strip().split('\t')

# output of preprocess.py
def readWordCount(path):
    wc = {}
    with open (path,'r') as f:
        for line in map(splice, f.readlines()):
            wc[line[0]] = int(line[1])
    return wc
        
# output of preprocess.py
def readTF(path):
    tf = {} ; current = None
    with open (path,'r') as f:
        for line in map(splice, f.readlines()):
            if len(line) != 3:
                continue
            if line[0] == current:
                tf[current][line[1]] = int(line[2])
            else:
                current = line[0]
                tf[current] = { line[1] : int(line[2]) }
    return tf

# output of preprocess.py
def readIDF(path):
    idf = {}
    with open (path,'r') as f:
        for line in map(splice, f.readlines()):
            if len(line) == 2:
                idf[line[0]] = float(line[1])
    return idf

# algorithm from wikipedia
def calcScore(D,Q,tfmap,idfmap,wcmap,k1,b):
    total = 0
    clean = re.sub(r'[^\s\w]+','',Q.lower())
    for qi in clean.split(' '):
        if qi not in tfmap[D]:
            continue
        tf = tfmap[D][qi]
        idf = idfmap[qi]
        wc = wcmap[D]
        avg = sum(wcmap[f] for f in wcmap) / float(len(wcmap))
        total += idf * tf * (k1+1) / (tf + k1 * (1 - b + b * wc / avg))
    return total        


if __name__ == '__main__':
    #D = sys.argv[1]
    Q = sys.argv[1]
    k1 = float(sys.argv[2])
    b = float(sys.argv[3])

    idfmap = readIDF(idfpath)
    tfmap = readTF(tfpath)
    wcmap = readWordCount(wordcountpath)
    files = os.listdir(inputdir)
    results = []
    for f in files:
        # calculate score for each document
        results += [(f,calcScore(f,Q,tfmap,idfmap,wcmap,k1,b))]
    results = sorted(results, key=lambda tup: tup[1],reverse=True)
    x = 1
    for result in results:
        score = math.ceil(result[1]*100.0)/100.0
        print str(x)+'. '+result[0]+'\t\t('+str(score)+')'
        x = x + 1
