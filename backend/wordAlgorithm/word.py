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

class Word(object):
    originalWord="";
    language = ""
    translatedWord="";
    category="";
    wordValue=0;
    extensions=[]
    progress = 0;
    wordDifficulty = 0;
    
def makeWord(language,originalWord,translatedWord,category,extensions,wordDifficulty):
    word = Word()
    word.originalWord = originalWord
    word.translatedWord = translatedWord
    word.category = category
    word.extensions = extensions
    word.wordDifficulty = wordDifficulty
    word.language = language
    return word


language = ""
originalWord = ""
translatedWord = ""
category = 0
extensions = ""
wordDifficulty = ""
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
        

        
        
        
        
        
        
        