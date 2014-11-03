#!/usr/bin/env python

import os
import sys
import re
import math

inputdir = '../Presidents/'

def skip0trigramify(phrase):
    strigrams = set()
    words = phrase.split()
    for i in range(len(words)-2):
        strigrams |= {frozenset({words[i],words[i+1],words[i+2]})}
    return strigrams

def skip1trigramify(phrase):
    strigrams = set()
    words = phrase.split()
    for i in range(len(words)-2):
        strigrams |= {frozenset({words[i],words[i+1],words[i+2]})}
        if i + 3 < len(words):
            strigrams |= {frozenset({words[i],words[i+1],words[i+3]})}
            strigrams |= {frozenset({words[i],words[i+2],words[i+3]})}
    return strigrams

def phrases(path):
    with open (path,'r') as f:
        full = re.sub(r'[^\s\w\n]+','',f.read().replace('.','\n').replace('\r','').lower())
        return [s.lstrip() for s in full.split('\n') if s != '' and s != ' ']

if __name__ == '__main__':
    query = sys.argv[1]
    skip = sys.argv[2]
    trigramify = locals()['skip'+skip+'trigramify'];
    querygrams = trigramify(query.lower())
    results = []
    for fname in os.listdir(inputdir):
        passagegrams = set()
        for phrase in phrases(inputdir+fname):
            passagegrams |= trigramify(phrase.lower())
        passageScore = len(querygrams & passagegrams) / float(len(passagegrams))
        queryScore = len(querygrams & passagegrams) / float(len(querygrams))
        try:
            score = 2 * passageScore * queryScore / (passageScore + queryScore)
        except ZeroDivisionError:
            score = 0
        results += [(fname,score)]
    results = sorted(results,key=lambda tup:tup[1],reverse=True)
    count = 1
    for result in results:
        if result[0][0] == '.':
            continue
        score = math.ceil(result[1]*1000.0)/1000.0
        print str(count)+'. '+result[0]+'\t('+str(score)+')'
        count = count+1

