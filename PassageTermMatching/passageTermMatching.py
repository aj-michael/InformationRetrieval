#!/usr/bin/env python

import os
import re
import string
import sys
import math

#input query from command prompt, as list of terms
query = sys.argv[1]
query = getTerms(query)

inputdir = '../BM25Scoring/'

#extract total number of documents from N.dat
ninput = 'N.dat'
with open (inputdir+ninput,'r') as f:
    N = int(f.read())

#extract term frequencies from dfcount.dat
dfcount = {}
with open (inputdir+dfcountinput,'r') as f:
    for line in map(lambda x: x.strip().split('\t'), f.readlines()):
        if len(line) == 2:
            dfcount[line[0]] = int(line[1])

#compute passage scores for each document
passageScores = {}            
for fname in os.listdir(input_dir):
    passageScores[fname] = passageScore(fname)

#print top 10 documents
sortedKeys = sorted(passageScores, key=passageScores.get)
for i in range(10):
    print(sortedKeys[i])

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

    #return passage score
    return numer / denom

# returns if the given passage contains the given file
def fileContains(term,passage):
    inputdir = '../Presidents'
    with open(inputdir+passage,'r') as f:
        return term in f

# returns the idf of the given term
def idf(term):
    return math.log(N/(dfcount[term]+1))

#converts input of string to list of terms
def getTerms(terms):
    outList = {}
    for word in terms.split(' '):
        outList.append(word)
    return outList
