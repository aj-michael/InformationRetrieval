#!/usr/bin/env python

import os
import re
import string
import sys
import math

specialTerms = [
        'civil war',
        'first president',
        'world war i',
        'world war ii',
        'great depression',
        'pearl harbor',
        'world trade center',
        'white house',
        'George Washington',
        'John Adams',
        'Thomas Jefferson',
        'James Madison',
        'James Monroe', 
        'John Quincy Adams', 
        'Andrew Jackson', 
        'Martin Van Buren', 
        'William H. Harrison', 
        'John Tyler', 
        'James K Polk', 
        'Zachary Taylor', 
        'Millard Fillmore', 
        'Franklin Pierce',
        'James Buchanan',
        'Abraham Lincoln',
        'Andrew Johnson',
        'Ulysses S Grant',
        'Rutherford B Hayes',
        'James A Garfield',
        'Chester A Arthur',
        'Grover Cleveland', 
        'Benjamin Harrison', 
        'Grover Cleveland', 
        'William McKinley', 
        'Theodore Roosevelt', 
        'William H Taft', 
        'Woodrow Wilson',
        'Warren G Harding',
        'Calvin Coolidge',
        'Herbert Hoover',
        'Franklin D Roosevelt',
        'Harry S Truman',
        'Dwight D Eisenhower',
        'John F Kennedy',
        'Lyndon B Johnson',
        'Richard M Nixon',
        'Gerald R Ford',
        'Jimmy Carter',
        'Ronald Reagan',
        'George H W Bush',
        'Bill Clinton',
        'George W Bush',
        'Barack H Obama',
    ]

#print specialTerms

# returns the passage score for a given passage
def passageScore(passage):
    numer = 0
    denom = 0
    contains = 0
    total = 0
    #compute numerator and denominator
    for term in query:
        wij = 0
        if fileContains(term,passage):
            wij = idf(term)
            contains += 1
        total += 1
        numer += wij
        denom += idf(term)
        #print term, ':', wij, idf(term), numer, denom

    #return passage score
    #if no words existed, return 0
    if total == 0:
        return 0.0
    #handle / 0 case, return fraction of words contained instead
    elif denom == 0:
        return contains / float(total)
    else:
        return numer / float(denom)

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
    tempWord = ""
    for word in terms.split(' '):
        word = word.lower()
        if tempWord == "":
            tempWord = word
        else:
            tempWord = tempWord + ' ' + word
        portion = False
        isWord = False
        for bigWord in specialTerms:
            bigWord = bigWord.lower()
            if tempWord == bigWord:
                isWord = True
                portion = False
                #print bigWord, tempWord
            elif bigWord.startswith(tempWord) and (bigWord[len(tempWord):][0] == ' '):
                portion = True
                #print bigWord, tempWord
        # if temp word was matched, use as key
        if isWord:
           word = tempWord
        # only update counts on unmatched words, or matched words
        if isWord or not portion:
            outList.append(word)
            tempWord = ""
    print outList
    return outList


#input query from command prompt, as list of terms
query = sys.argv[1]
query = getTerms(query)

inputdir = '../PassageTermMatching/data/'

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
    print sortedKeys[i], passageScores[sortedKeys[i]]
