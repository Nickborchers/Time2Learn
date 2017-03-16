import word
#import numpy
import wordValueTable
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

# make array of words

# create new sorted array of words
# soting based on 

#wordValue = frequencyOfLetterinLanguage + wordlenght + correlation
#correlation = common letters + letters in same place - missplaced letters 

# Correlation calculation
def correlation(originalWord,translation):
    n = 0
    u = zip(originalWord,translation)
    for i,j in u:
        if i!=j:
            n+=1
    return n
    
#def correlation(originalWord, translation):
#	print numpy.corrcoef(originalWord, translation)[0, 1]

# Create and populate word queue
q = Q.PriorityQueue()
words = word.words
letterTable = wordValueTable.letterTable
letterValues = []

# Populate word queue
for word in words:
    language = word.language
    valuesPosition = 2+letterTable[1].index(language);
    letterValues = letterTable[valuesPosition]
    word.wordValue = len(word.originalWord)
    for c in word.originalWord:
        word.wordValue += float(letterValues[ord(c)-ord("a")])
    word.wordValue = correlation(word.originalWord,word.translatedWord)  #minimal correltion will be further developed
    
    
    
for w in words:
    q.put((w.wordValue,w))
