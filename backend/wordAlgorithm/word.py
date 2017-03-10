class Word(object):
    originalWord="esgbtntyht";
    language = ""
    translatedWord="";
    category="";
    wordValue=0;
    extensions=[]
    progress = 0;
    wordDifficulty = 0;
    
def makeWord(originalWord,translatedWord,category,wordValue,extensions,progress,wordDifficulty,language):
    word = Word()
    word.originalWord = originalWord
    word.translatedWord = translatedWord
    word.category = category
    word.wordValue = wordValue
    word.extensions = extensions
    word.progress = progress
    word.wordDifficulty = wordDifficulty
    word.language = language
    return word