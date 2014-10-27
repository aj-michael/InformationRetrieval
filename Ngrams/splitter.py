#!/usr/bin/env python

import os
import sys
import re

inputdir = '../Presidents/'
outputdir = 'ngrams/'

def ngramify(text,N):
    ngrams = {}
    words = text.split(' ')
    for i in range(len(words)+1-N):
        ngram =  ' '.join([words[i+j] for j in range(N)])
        ngrams[ngram] = ngrams[ngram] + 1 if ngram in ngrams.keys() else 1
    return ngrams

def getText(path):
    with open (path,'r') as f:
        text = re.sub(r'[^\s\w]+','',f.read().replace('\r',' ').replace('\n',' ').replace('\t',' ').lower())
        return ' '.join(text.split())

def writeNgramFile(path,ngrams):
    with open (path,'w+') as f:
        for ngram,count in ngrams.iteritems():
            f.write(ngram+'\t'+str(count)+'\n')

if __name__ == '__main__':
    N = int(sys.argv[1])
    for fname in os.listdir(inputdir):
        inpath = inputdir+fname
        outpath = outputdir+str(N)+'grams/'+fname
        ngrams = ngramify(getText(inpath),N)
        if not os.path.exists(os.path.dirname(outpath)):
            os.makedirs(os.path.dirname(outpath))
        writeNgramFile(outpath,ngrams)
