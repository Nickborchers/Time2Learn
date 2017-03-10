import word
import wordValueTable

#read xml
import xml.etree.ElementTree
e = xml.etree.ElementTree.parse('words2.xml').getroot()

# make array of words

# create new sorted array of words
# soting based on 

#wordValue = frequencyOfLetterinLanguage + wordlenght + correlation
#correlation = common letters + letters in same place - missplaced letters 
w = word.makeWord("trololo","","","","","",0)
print(w.originalWord);

#word length
#value of the word
# char originalWord, char translatedWord, char category, int wordValue,char[] extensions,int progress,int wordDifficulty, char[] language