#!/usr/bin/env python

import math
import os
import re
import string

inputdir = '../Presidents/'
tfcountout = 'data/tfcount.dat'
dfcountout = 'data/dfcount.dat'
totaldocsout = 'data/N.dat'
wordcountout = 'data/wordcount.dat'
idfout = 'data/idf.dat'

exclude = set(string.punctuation)

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

def calcTfDfWcN(path):
    dfcount = {}
    tfcount = {}
    wordcount = {}
    N = len(os.listdir(path))
    for fname in os.listdir(path):
        tfcount[fname] = {}
        with open (path+fname,'r') as f:
            text = re.sub(r'[^\s\w]+','',f.read().replace('\r',' ').replace('\n',' ').replace('\t',' ').lower())
            wordcount[fname] = len(text.split(' '))
            tempWord = ""
            for word in text.split(' '):
                if '/t' not in word and word != '':
                    if tempWord == '':
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
                        if word in dfcount.keys():
                            dfcount[word] = dfcount[word] | {fname}
                        else:
                            dfcount[word] = {fname}
                        if word in tfcount[fname].keys():
                            tfcount[fname][word] = tfcount[fname][word] + 1
                        else:
                            tfcount[fname][word] = 1
                        tempWord = ""
    dfcount = {key:len(value) for key,value in dfcount.iteritems()}
    return tfcount,dfcount,wordcount,N


def calcNqi(qi,dfcount):
    return dfcount[qi] if qi in dfcount.keys() else 0

def calcIDF(N,nqi):
    return math.log((N-nqi+0.5)/(nqi+0.5))


# write tf vector
def writeTf(path,tf):
    with open (path,'w+') as f:
        for fname in tf:
            for word in tf[fname]:
                f.write(fname+'\t'+word+'\t'+str(tf[fname][word])+'\n')

# write df vector
def writeDf(path,df):
    with open (path,'w+') as f:
        for word,count in df.iteritems():
            f.write(word+'\t'+str(count)+'\n')
        #for word,fileset in df.iteritems():
        #    f.write(word+'\t'+str(len(fileset))+'\n')

# write N
def writeN(path,N):
    with open (path,'w+') as f:
        f.write(str(N))

# write wc vector
def writeWc(path,wc):
    with open (path,'w+') as f:
        for fname,count in wc.iteritems():
            f.write(fname+'\t'+str(count)+'\n')

# write idf vector
def writeIdf(path,df,N):
    with open (idfout,'w+') as f:
        for word,count in df.iteritems():
            nqi = calcNqi(word,df)
            IDF = max(0,calcIDF(N,nqi))
            f.write(word+'\t'+str(IDF)+'\n')

if __name__ == '__main__':
    tf,df,wc,N = calcTfDfWcN(inputdir)
    writeTf(tfcountout,tf)
    writeDf(dfcountout,df)
    writeWc(wordcountout,wc)
    writeN(totaldocsout,N)
    writeIdf(idfout,df,N)
    
