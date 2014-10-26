#!/usr/bin/env python

import os
import re
import string

input_dir = '../Presidents/'
output = 'dfcount.dat'

exclude = set(string.punctuation)

dfcount = {}
for fname in os.listdir(input_dir):
    with open (input_dir+fname,'r') as f:
        text = re.sub(r'[^\s\w]+','',f.read().replace('\r','').replace('\n','').replace('\t','').lower())
        for word in text.split(' '):
            if word in dfcount.keys():
                dfcount[word] = dfcount[word] + 1
            else:
                dfcount[word] = 1
with open (output,'w+') as f:
    for word,count in dfcount.iteritems():
        f.write(word+'\t'+str(count)+'\n')
