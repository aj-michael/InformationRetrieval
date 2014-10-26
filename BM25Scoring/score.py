#!/usr/lib/env python

import sys

def readIDF(path):
     

def score(D,Q,tfmap,idfmap,k1,b):
    total = 0
    for qi in Q:
        if qi not in tfmap[D].keys():
            pass
        tf = tfmap[D][qi]
        idf = idfmap[qi]
        total += idf * tf * (k1+1) / (tf + k1 * (1 - b + b * 
        

if __name__ == '__main__':
    D = sys.argv[1]
    Q = sys.argv[2]
    for qi in Q:
        print qi
