#!/usr/bin/env python

import os
import sys
import re
import math

inputdir = '../Presidents/'

# split phrase into set of 0-skip 2-grams
def skip0bigramify(phrase):
    sbigrams = set()
    words = phrase.split()
    for i in range(len(words)-1):
        sbigrams |= {frozenset({words[i],words[i+1]})}
    return sbigrams

# split phrase into set of 1-skip 2-grams
def skip1bigramify(phrase):
    sbigrams = set()
    words = phrase.split()
    for i in range(len(words)-1):
        sbigrams |= {frozenset({words[i],words[i+1]})}
        if i + 2 < len(words):
            sbigrams |= {frozenset({words[i],words[i+2]})}
    return sbigrams

# split phrase into set of 2-skip 2-grams
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
        full = re.sub(r'[^\s\w\n]+','',f.read().replace('.','\n').replace('\r','').lower())
        return [s.lstrip() for s in full.split('\n') if s != '' and s != ' ']


if __name__ == '__main__':
    query = sys.argv[1]
    skip = sys.argv[2]
    bigramify = locals()['skip'+skip+'bigramify'];
    querygrams = bigramify(query.lower())
    results = []
    for fname in os.listdir(inputdir):
        passagegrams = set()
        for phrase in phrases(inputdir+fname):
            passagegrams |= bigramify(phrase.lower())
        # calculate score_p and score_q
        passageScore = len(querygrams & passagegrams) / float(len(passagegrams))
        queryScore = len(querygrams & passagegrams) / float(len(querygrams))
        try:
            score = 2 * passageScore * queryScore / (passageScore + queryScore)
        except ZeroDivisionError:
            # we don't include these results in the analysis
            score = 0
        results += [(fname,score)]

    # sort results
    results = sorted(results,key=lambda tup:tup[1],reverse=True)
    count = 1
    for result in results:
        if result[0][0] == '.':
            continue
        # truncate to 3 decimal places for display purposes
        score = math.ceil(result[1]*1000.0)/1000.0
        print str(count)+'. '+result[0]+'\t('+str(score)+')'
        count = count+1
