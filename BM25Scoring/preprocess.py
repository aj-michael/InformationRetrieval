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
            for word in text.split(' '):
                if word in dfcount.keys():
                    dfcount[word] = dfcount[word] | {fname}
                else:
                    dfcount[word] = {fname}
                if word in tfcount[fname].keys():
                    tfcount[fname][word] = tfcount[fname][word] + 1
                else:
                    tfcount[fname][word] = 1
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
            IDF = calcIDF(N,nqi)
            f.write(word+'\t'+str(IDF)+'\n')

if __name__ == '__main__':
    tf,df,wc,N = calcTfDfWcN(inputdir)
    writeTf(tfcountout,tf)
    writeDf(dfcountout,df)
    writeWc(wordcountout,wc)
    writeN(totaldocsout,N)
    writeIdf(idfout,df,N)
    
