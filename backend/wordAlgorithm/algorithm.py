import word
import wordValueTable

# make array of words

# create new sorted array of words
# soting based on 

#wordValue = frequencyOfLetterinLanguage + wordlenght + correlation
#correlation = common letters + letters in same place - missplaced letters 
#print letterTable
#w = word.makeWord("trololo","","","","","",0)
#print(w.originalWord);
language = "Dutch" #language can be taken from word object xml
letterTable = wordValueTable.letterTable
letterValues = []
print letterTable[1].index(language)
valuesPosition = 2+letterTable[1].index(language);
letterValues = letterTable[valuesPosition]
print letterValues

#word length
#value of the word
# char originalWord, char translatedWord, char category, int wordValue,char[] extensions,int progress,int wordDifficulty, char[] language