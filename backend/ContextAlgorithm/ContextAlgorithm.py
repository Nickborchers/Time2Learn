import requests
import xml.etree.cElementTree as ET
import string

INPUT_LANG = 'es'
OUTPUT_LANG = 'en'
WORD = 'cama'
WORD_DIFFICULTY = 882
TITLE = 'SpanishWordFrequencies'
PATH = "/home/antonio/Desktop/SE/FrecuencyList/" + TITLE + ".xml"
MAX_LENGTH_SENTENCE = 15


#Class sentence which contains:
#   -the sentence(self.sentenceString)
#   -words in the sentence(self.words)
#   -values of each word(self.wordValues)
#   -total difficulty of the sentence(self.difficulty)
class Sentence:


    def __init__(self, sentenceString, words):
        self.sentenceString = sentenceString
        self.words = words
        self.wordsValues = []
        self.difficulty = 0


    def addValues(self, values):
        self.wordsValues = values


    def setDifficulty(self, difficulty):
        self.difficulty = difficulty


    def __str__(self):
        return self.sentenceString

#Delete inneccesary symbols
def cleanSentence(sentence):
    sentence = sentence.replace('[...] ', '')
    sentence = sentence.replace('"', '')
    sentence = sentence.replace('/', '')
    return sentence

#Delete the punctuation of a sentence
def deletePunctuation(sentence):
    punctuationDeleter = str.maketrans('', '', string.punctuation)
    sentence = sentence.translate(punctuationDeleter)
    sentence = sentence.replace('¿', '')
    sentence = sentence.replace('¡', '')
    return sentence

#Calculates the error regarding the word difficulty
def errorCalculation(wordsValues):
    error=0
    for x in range(0, len(wordsValues)):
        error += wordsValues[x] - WORD_DIFFICULTY

    error /= len(wordsValues)

    return error

#Calculates the difficult value for each word in a sentence
def calculateSentenceWordsValue(root, sentence):
    wordValues=[]
    for j in range(0, len(sentence.words)):
        try:
            wordValues.append(int(root.find(sentence.words[j].lower()).text))
        except AttributeError:
            wordValues.append(WORD_DIFFICULTY)

    return wordValues

#Returns the simpler and the most challenging sentences
def betterSentences(possibleSentences):
    challengingSentence = ""
    simplestSentence = ""
    min = float("-inf")
    max = float("inf")

    for s in possibleSentences:
        if s.difficulty > min:
            min = s.difficulty
            challengingSentence = s.sentenceString

        if s.difficulty < max:
            max = s.difficulty
            simplestSentence = s.sentenceString

    return challengingSentence, simplestSentence


def main():
    resp = requests.get('https://linguee-api.herokuapp.com/api?q=' + WORD + '&src=' + INPUT_LANG + '&dst=' + OUTPUT_LANG)
    output = resp.json()

    sentences = []


    try:
        for example in output ['real_examples']:
            sentences.append(cleanSentence(sentence = example['src']))
    except KeyError:
        print("Word not found in api")
        exit()

    currentSentence = ""
    root = ET.parse(PATH).getroot()
    possibleSentences = []


    print("The possible sentences are:")
    for i in range(0, len(sentences)):
        sentenceWords = deletePunctuation(sentences[i]).split()
        sentence = Sentence(sentences[i], sentenceWords)
        sentence.addValues(calculateSentenceWordsValue(root, sentence))
        sentence.setDifficulty(errorCalculation(sentence.wordsValues))

        if len(sentence.words) <= MAX_LENGTH_SENTENCE and (int (sentence.difficulty)) <= WORD_DIFFICULTY:
            possibleSentences.append(sentence)
            print(sentence)


    challengingSentence,simplestSentence = betterSentences(possibleSentences)
    print("\nThe most challenging sentence is:\n", challengingSentence, "\nThe simplest sentence is:\n",  simplestSentence)

if __name__ == "__main__":
    main()



