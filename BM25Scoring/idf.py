#!/usr/bin/env python

import sys
import math

ninput = 'N.dat'
dfcountinput = 'dfcount.dat'

if not len(sys.argv) == 2:
    print 'Include exactly one argument'
    exit(0)

qi = sys.argv[1]

with open (ninput,'r') as f:
    N = int(f.read())

dfcount = {}
with open (dfcountinput,'r') as f:
    for line in map(lambda x: x.strip().split('\t'), f.readlines()):
        if len(line) == 2:
            dfcount[line[0]] = int(line[1])

nqi = dfcount[qi] if qi in dfcount.keys() else 0

IDF = math.log((N-nqi+0.5)/(nqi+0.5))

print "IDF = ", IDF

