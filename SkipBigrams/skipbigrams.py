#!/usr/bin/env python

import os
import sys
import re

inputdir = '../Presidents/'
outputdir = 'skipbigrams/'

def skip1bigramify(phrase):
    sbigrams = set()
    words = phrase.split()
    for i in range(len(words)-1):
        sbigrams |= {frozenset({words[i],words[i+1]})}
        if i + 2 < len(words):
            sbigrams |= {frozenset({words[i],words[i+2]})}
    return sbigrams

def skip2bigramify(phrase):
    sbigrams = set()
    words = phrase.split()
    for i in range(len(words)-1):
        sbigrams |= {frozenset({words[i],words[i+1]})}
        if i + 2 < len(words):
            sbigrams |= {frozenset({words[i],words[i+2]})}
        if i + 3 < len(words):
            sbigrams |= {frozenset({words[i],words[i+3]})}
    return sbigrams

def phrases(path):
    with open (path,'r') as f:
        full = re.sub(r'[^\s\w\n]+','',f.read().replace('.','\n').replace('\r',''))
        return [s.lstrip() for s in full.split('\n') if s != '' and s != ' ']


if __name__ == '__main__':
    query = sys.argv[1]
    skip = int(sys.argv[2])
    bigramify = skip2bigramify if skip == 2 else skip1bigramify
    querygrams = bigramify(query)
    print querygrams
    results = []
    for fname in os.listdir(inputdir):
        passagegrams = set()
        for phrase in phrases(inputdir+fname):
            passagegrams |= bigramify(phrase)
        passageScore = len(querygrams & passagegrams) / float(len(passagegrams))
        queryScore = len(querygrams & passagegrams) / float(len(querygrams))
        try:
            score = 2 * passageScore * queryScore / (passageScore + queryScore)
        except ZeroDivisionError:
            score = 0
        results += [(fname,score)]
    results = sorted(results,key=lambda tup:tup[1],reverse=True)
    for result in results:
        print result
