import math
import re
from os import listdir
from os.path import join

SPAM_PROB = 0.6
HAM_PROB = 1 - SPAM_PROB

def allWords(text): return re.findall('[a-z]+', text.lower()) 

def makeCountsDictFromDir(dirname):
    filenames = listdir(dirname)
    output = {}
    for filename in filenames:
        f = open(join(dirname, filename), "r") 
        words = allWords(f.read())
        for word in words:
            output[word] = output.get(word, 0) + 1
        f.close()
    return output

SpamWordCounts = makeCountsDictFromDir("spam")
HamWordCounts = makeCountsDictFromDir("ham")

SpamWords = sum(SpamWordCounts.values())
HamWords = sum(HamWordCounts.values())

def probOfSpamGivenWord(word):
    probOfWordGivenSpam = (SpamWordCounts.get(word, 0)+ 1)/float(SpamWords + 1)
    probOfWordGivenHam = (HamWordCounts.get(word, 0) + 1)/float(HamWords + 1)
    probOfWord = SPAM_PROB*probOfWordGivenSpam + HAM_PROB*probOfWordGivenHam
    return (probOfWordGivenSpam*SPAM_PROB)/probOfWord

def probOfSpamGivenMessage(msg):
    probs = [probOfSpamGivenWord(word) for word in re.findall('[a-z]+', msg.lower())]
    n = 0
    for p in probs:
        n += (math.log(1 - p) - math.log(p))
    return 1/(1 + math.exp(n))
    
msg = ""

print(probOfSpamGivenMessage(msg))
