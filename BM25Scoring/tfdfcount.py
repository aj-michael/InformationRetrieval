#!/usr/bin/env python

import os
import re
import string

inputdir = '../Presidents/'
tfcountout = 'tfcount.dat'
dfcountout = 'dfcount.dat'
totaldocsout = 'N.dat'

exclude = set(string.punctuation)
dfcount = {}
tfcount = {}
for fname in os.listdir(inputdir):
    tfcount[fname] = {}
    with open (inputdir+fname,'r') as f:
        text = re.sub(r'[^\s\w]+','',f.read().replace('\r','').replace('\n','').replace('\t','').lower())
        for word in text.split(' '):
            if word in dfcount.keys():
                dfcount[word] = dfcount[word] | {fname}
            else:
                dfcount[word] = {fname}
            if word in tfcount[fname].keys():
                tfcount[fname][word] = tfcount[fname][word] + 1
            else:
                tfcount[fname][word] = 1

with open (tfcountout,'w+') as f:
    for fname in tfcount:
        for word in tfcount[fname]:
            f.write(fname+'\t'+word+'\t'+str(tfcount[fname][word])+'\n')

with open (dfcountout,'w+') as f:
    for word,fileset in dfcount.iteritems():
        f.write(word+'\t'+str(len(fileset))+'\n')

with open (totaldocsout,'w+') as f:
    f.write(str(len(os.listdir(inputdir))))
