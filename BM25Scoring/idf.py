#!/usr/bin/env python

import math

ninput = 'N.dat'
dfcountinput = 'dfcount.dat'
idfout = 'idf.dat'

def readdfcount(path):
    dfcount = {}
    with open (path,'r') as f:
        for line in map(lambda x: x.strip().split('\t'), f.readlines()):
            if len(line) == 2:
                dfcount[line[0]] = int(line[1])
    return dfcount

def readN(path):
    with open (path,'r') as f:
        return int(f.read())

def calcNqi(qi,dfcount):
    return dfcount[qi] if qi in dfcount.keys() else 0

def calcIDF(N,nqi):
    return math.log((N-nqi+0.5)/(nqi+0.5))

if __name__ == '__main__':
    N = readN(ninput)
    dfcount = readdfcount(dfcountinput)
    with open (idfout,'w+') as f:
        for word,count in dfcount.iteritems():
            nqi = calcNqi(word,dfcount)
            IDF = calcIDF(N,nqi)
            f.write(word+'\t'+str(IDF)+'\n')
