import sys
import os
import string
import json
import math
from collections import Counter


# In[2]:

file_train = sys.argv[1]
file_label = sys.argv[2]

dict_labels = {}

filename = open(file_label,'r')

for lines in filename:
    line = lines.split()
    key = line[0]
    TD = line[1]
    PN = line[2] 
    dict_labels[key] = TD, PN 

dict_words = {}
filename.close()

filename2 = open(file_train, 'r')

lines = filename2.readlines()

for line in lines:
    words = line.split()
    key = words[0]
    wordlist = words[1::]
    #wordlist = filter(lambda i: not str.isdigit(i), wordlist)
    dict_words[key] = wordlist
filename2.close()

c = Counter(dict_labels.values())

D_prior = (c[('deceptive','negative')]+ c[('deceptive','positive')])*1.0/sum(c.values())
T_prior = (c[('truthful','negative')]+ c[('truthful','positive')])*1.0/sum(c.values())
P_prior = (c[('deceptive','positive')]+ c[('truthful','positive')])*1.0/sum(c.values())
N_prior = (c[('deceptive','negative')]+ c[('truthful','negative')])*1.0/sum(c.values())

model = {}
model['Prior'] = {}
model['Prior']['deceptive'] = D_prior
model['Prior']['truthful'] = T_prior
model['Prior']['positive'] = P_prior
model['Prior']['negative'] = N_prior
            
deceptive_words = []
truthful_words = []
positive_words = []
negative_words = []
        
for key in dict_labels.keys():
            if dict_labels[key] == ('deceptive','negative'):
                words = dict_words[key];
                for word in words:
                    word = word.translate(None, string.punctuation)
                    #word = ''.join(x for x in word if x not in string.punctuation)
                    deceptive_words.append(word.lower())
                    negative_words.append(word.lower())
            if dict_labels[key] == ('deceptive','positive'):
                words = dict_words[key];
                for word in words:
                    word = word.translate(None, string.punctuation)
                    #word = ''.join(x for x in word if x not in string.punctuation)
                    deceptive_words.append(word.lower())
                    positive_words.append(word.lower())
            if dict_labels[key] == ('truthful','negative'):
                words = dict_words[key];
                for word in words:
                    word = word.translate(None, string.punctuation)
                    #word = ''.join(x for x in word if x not in string.punctuation)
                    truthful_words.append(word.lower())
                    negative_words.append(word.lower())
            if dict_labels[key] == ('truthful','positive'):
                words = dict_words[key];
                for word in words:
                    word = word.translate(None, string.punctuation)
                    #word = ''.join(x for x in word if x not in string.punctuation)
                    truthful_words.append(word.lower())
                    positive_words.append(word.lower())        

vocabulary = set(deceptive_words + truthful_words)
 
#stop_words =[" "]

stop_words = set([" ", "a","about","above","all","am","an","and","are","as","at","be","been","being","between","both","by","could","did","do","does","doing","during","each","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","my","myself","of","on","once","only","or","other","ought","our","ours    ourselves","out","own","same","shan't","she","she'd","she'll","she's","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","until","up","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","would","you","you'd","you'll","you're","you've","your","yours""yourself","yourselves"])

deceptive_words = [x for x in deceptive_words if x not in stop_words]
truthful_words = [x for x in truthful_words if x not in stop_words]
positive_words = [x for x in positive_words if x not in stop_words]
negative_words = [x for x in negative_words if x not in stop_words]

dec_count = Counter(deceptive_words)
tru_count = Counter(truthful_words)    
pos_count = Counter(positive_words)
neg_count = Counter(negative_words)


model['deceptive'] = {}
model['truthful'] = {}
model['positive'] = {}
model['negative'] = {}

for word in vocabulary:
    
    dec_countf = 1 + dec_count[word]
    tru_countf = 1 + tru_count[word]
    pos_countf = 1 + pos_count[word]
    neg_countf = 1 + neg_count[word]
    
    model['deceptive'][word] = (dec_countf * 1.0) /(len(deceptive_words) +len(vocabulary))
    model['truthful'][word] = (tru_countf * 1.0) /(len(truthful_words) +len(vocabulary))
    model['positive'][word] = (pos_countf * 1.0) /(len(positive_words) +len(vocabulary))
    model['negative'][word] = (neg_countf * 1.0) /(len(negative_words) +len(vocabulary))


o = open('nbmodel.txt', 'w+');
json.dump(model, o)
o.close()