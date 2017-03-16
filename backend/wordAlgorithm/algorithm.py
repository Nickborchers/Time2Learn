import word
import wordValueTable
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

# This algorithm makes an array of words and creates a new sorted array of words

# Correlation calculation according to the Levenshtein-Algorithm (multiplied with the correct factor)
def correlation(originalWord, translation):
    originalWord = list(originalWord)
    translation = list(translation)
    lenOrignalWord = len(originalWord)+1
    lenTranslation = len(translation)+1
    matrix = [[0 for x in range(lenTranslation)] for y in range(lenOrignalWord)] 
    for i in range(1, lenOrignalWord):
        matrix[i][0] = i
    for j in range(1, lenTranslation):
        matrix[0][j] = j
    
    for j in range (1, lenTranslation):
        for i in range (1, lenOrignalWord):
            if (originalWord[i-1] == translation[j-1]):
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1] + cost)

    return 100*matrix[i][j] 


# Create and populate word queue
q = Q.PriorityQueue()
words = word.words
letterTable = wordValueTable.letterTable
letterValues = []

# Populate word queue with word values
# Word values depend on:
# 1. number of letters in a word
# 2. frequency of letters in a language (according to a table) compared with the word
# 3. the correlation of the word with its translation
# 4. how common a word is (yet to be implemented)
for word in words:
    language = word.language
    valuesPosition = 2+letterTable[1].index(language);
    letterValues = letterTable[valuesPosition]
    word.wordValue = len(word.originalWord)
    for c in word.originalWord:
        word.wordValue += float(letterValues[ord(c)-ord("a")])

    word.wordValue += correlation(word.originalWord,word.translatedWord)  
    
# Put the word objects in the queue in increasing order of the word value    
for w in words:
    q.put((w.wordValue, w))
