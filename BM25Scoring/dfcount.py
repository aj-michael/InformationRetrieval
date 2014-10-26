#!/usr/bin/env python

import os
import re
import string

inputdir = '../Presidents/'
dfcountout = 'dfcount.dat'
totaldocsout = 'N.dat'

exclude = set(string.punctuation)
dfcount = {}
for fname in os.listdir(inputdir):
    with open (inputdir+fname,'r') as f:
        text = re.sub(r'[^\s\w]+','',f.read().replace('\r','').replace('\n','').replace('\t','').lower())
        for word in text.split(' '):
            if word in dfcount.keys():
                dfcount[word] = dfcount[word] + 1
            else:
                dfcount[word] = 1
with open (dfcountout,'w+') as f:
    for word,count in dfcount.iteritems():
        f.write(word+'\t'+str(count)+'\n')
with open (totaldocsout,'w+') as f:
    f.write(str(len(os.listdir(inputdir))))
