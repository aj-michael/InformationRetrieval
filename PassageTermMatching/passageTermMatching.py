#!/usr/bin/env python

import os
import re
import string
import sys
import math

# returns the passage score for a given passage
def passageScore(passage):
    numer = 0
    denom = 0
    #compute numerator and denominator
    for term in query:
        wij = 0
        if fileContains(term,passage):
            wij = idf(term)
        numer += wij
        denom += idf(term)
        #print term, ':', wij, idf(term), numer, denom

    #return passage score
    return numer / denom

# returns if the given passage contains the given file
def fileContains(term,passage):
    return term in containsLists[passage]

# returns the idf of the given term
def idf(term):
    c = 0
    if term in dfcount.keys():
        c = dfcount[term]
    #print c, N, math.log(N/float(c+1))
    return math.log(N/float(c+1))

#converts input of string to list of terms
def getTerms(terms):
    outList = []
    for word in terms.split(' '):
        outList.append(word.lower())
    return outList

#input query from command prompt, as list of terms
query = sys.argv[1]
query = getTerms(query)

inputdir = '../BM25Scoring/data/'

#extract total number of documents from N.dat
ninput = 'N.dat'
with open (inputdir+ninput,'r') as f:
    N = int(f.read())

#extract term frequencies from dfcount.dat
dfcount = {}
dfcountinput = 'dfcount.dat'
with open (inputdir+dfcountinput,'r') as f:
    for line in map(lambda x: x.strip().split('\t'), f.readlines()):
        if len(line) == 2:
            dfcount[line[0]] = int(line[1])

#extract contains list from dfcount.dat
containsLists = {}
tfcountinput = 'tfcount.dat'
with open (inputdir+tfcountinput,'r') as f:
    for line in map(lambda x: x.strip().split('\t'), f.readlines()):
        if len(line) == 3:
            if line[0] not in containsLists.keys():
                containsLists[line[0]] = []
            containsLists[line[0]].append(line[1])

#compute passage scores for each document
passageScores = {}
inputdir = '../Presidents/'
for fname in os.listdir(inputdir):
    passageScores[fname] = passageScore(fname)

#print top 10 documents
sortedKeys = sorted(passageScores, key=passageScores.get,reverse=True)
print(passageScores),'\n\n'
for i in range(10):
    print(sortedKeys[i])
