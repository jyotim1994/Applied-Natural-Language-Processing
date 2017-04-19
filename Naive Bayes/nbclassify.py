import sys
import string
import json
import math


o = open('nbmodel.txt', 'r')
data = json.load(o)
o.close()

file_name = sys.argv[1]

test_file = open(file_name, 'r')

dict_words = {}

lines = test_file.readlines()

for line in lines:
    words = line.split()
    key = words[0]
    wordlist = words[1::]
    #wordlist = filter(lambda i: not str.isdigit(i), wordlist)
    dict_words[key] = wordlist

test_file.close()
#stop_words =[" "]

stop_words = set([" ", "a","about","above","all","am","an","and","are","as","at","be","been","being","between","both","by","could","did","do","does","doing","during","each","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","my","myself","of","on","once","only","or","other","ought","our","ours    ourselves","out","own","same","shan't","she","she'd","she'll","she's","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","until","up","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","would","you","you'd","you'll","you're","you've","your","yours""yourself","yourselves"])

testwords = []

output_words = {}


for key in dict_words.keys():
    words = dict_words[key]
    
    dec_prob = 0
    tru_prob = 0
    pos_prob = 0
    neg_prob = 0

    for word in words:
        word = word.translate(None, string.punctuation)
        word = word.lower()
       
       	if word in stop_words:
        	continue
       
        if word in data['deceptive']:
            dec_prob += math.log(data['deceptive'][word], 10)
        if word in data['truthful']:
            tru_prob += math.log(data['truthful'][word], 10)
        if word in data['positive']:
            pos_prob += math.log(data['positive'][word], 10)
        if word in data['negative']:
            neg_prob += math.log(data['negative'][word], 10)
	
    dec_prob += math.log(data['Prior']['deceptive'], 10)
    tru_prob += math.log(data['Prior']['truthful'], 10) 
    pos_prob += math.log(data['Prior']['positive'], 10) 
    neg_prob += math.log(data['Prior']['negative'], 10)
    
    if dec_prob > tru_prob:
        TD = "deceptive"
    else: 
        TD = "truthful"
    
    if pos_prob > neg_prob:
        PN = "positive"
    else:
        PN = "negative"
    
    output_words[key] = TD, PN    
        
test_file = open(file_name, 'r')
output = open('nboutput.txt', 'w+')    
lines = test_file.readlines()

for line in lines:
    words = line.split()
    key = words[0]
    output.write(key + ' ' + output_words[key][0] + ' ' + output_words[key][1] + '\n')   
    
test_file.close()
output.close()       