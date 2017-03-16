# Format of xml taken as input:
#    <Words>
#        <Word>
#            <Language>Dutch</Language>
#            <Word>ja</Word>
#            <Translation>yes</Translation>
#            <Category/>
#            <Word_Difficulty/>
#            <Extensions/>
#        </Word>
#    </Words>


words = []

# Word object
class Word(object):
    originalWord="";
    language = ""
    translatedWord="";
    category="";
    wordValue=0;
    extensions=[]
    progress = 0;
    wordDifficulty = 0;
    
# Word constructor
def makeWord(language,originalWord,translatedWord,category,extensions,wordDifficulty):
    word = Word()
    word.originalWord = originalWord
    word.translatedWord = translatedWord
    word.category = category
    word.extensions = extensions
    word.wordDifficulty = wordDifficulty
    word.language = language
    return word

def checkExistance (value):
    if not (value is None):
        return value
    return ""

# Word printer
def printWord(word):
    print "Language: " + checkExistance(word.language)
    print "Original Word: " + checkExistance(word.originalWord)
    print "Translated Word: " + checkExistance(word.translatedWord)
    print "Category: " + checkExistance(word.category)
    print "Extensions: " + checkExistance(word.extensions)
    print "Word Difficulty: " + checkExistance(word.wordDifficulty)


language = ""
originalWord = ""
translatedWord = ""
category = 0
extensions = ""
wordDifficulty = ""

# XML parsing
import xml.etree.ElementTree as ET
tree = ET.parse('words.xml');
root = tree.getroot()
for child in root:
    for child1 in child:
        if child1.tag == "Language":
            language = child1.text
            
        if child1.tag == "Word":
            originalWord = child1.text
            
        if child1.tag == "Translation":
            translatedWord = child1.text
            
        if child1.tag == "Category":
            category = child1.text
            
        if child1.tag == "Word_Difficulty":
            extensions = child1.text
            
        if child1.tag == "Extensions":
            wordDifficulty = child1.text
    words.append(makeWord(language,originalWord,translatedWord,category,extensions,wordDifficulty))
        

        
        
        
        
        
        
        
