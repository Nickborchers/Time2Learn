import requests
import xml.etree.cElementTree as et
import string
import os
import operator

OUTPUT_LANG = 'en'

# These three values will be filled by the input when it will be implemented
INPUT_LANG = 'es'
WORD = ''
WORD_DIFFICULTY = 0

POSSIBLE_TITLE_FREQ = ['SpanishWordFrequencies.xml', 'DutchWordFrequencies.xml', 'GermanWordFrequencies.xml']
POSSIBLE_LANGUAGES = ['es', 'nl', 'de']
TITLE_FREQ = 'SpanishWordFrequencies.xml'
TITLE_SHORTED_WORDS = 'result.xml'
PATH_FREQ_LIST = "/home/antonio/Desktop/SE/FrecuencyList/"
PATH_INPUT_WORDS = ''
MAX_LENGTH_SENTENCE = 15


# Class sentence which contains:
#   -the sentence(self.sentence_string)
#   -words in the sentence(self.words)
#   -values of each word(self.word_values)
#   -total difficulty of the sentence(self.difficulty)

class Sentence:
    def __init__(self, sentence_string, words):
        self.sentence_string = sentence_string
        self.words = words
        self.words_values = []
        self.difficulty = 0

    def add_values(self, values):
        self.words_values = values

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def __str__(self):
        return self.sentence_string


def choose_language(language):
    global INPUT_LANG, TITLE_FREQ
    if language == 'Spanish':
        INPUT_LANG = POSSIBLE_LANGUAGES[0]
        TITLE_FREQ = POSSIBLE_TITLE_FREQ[0]
    elif language == 'Dutch':
        INPUT_LANG = POSSIBLE_LANGUAGES[1]
        TITLE_FREQ = POSSIBLE_TITLE_FREQ[1]
    else:
        INPUT_LANG = POSSIBLE_LANGUAGES[2]
        TITLE_FREQ = POSSIBLE_TITLE_FREQ[2]
    return


# Delete inneccesary symbols
def clean_sentence(sentence):
    sentence = sentence.replace('[...] ', '')
    sentence = sentence.replace('"', '')
    sentence = sentence.replace('/', '')
    return sentence


# Delete the punctuation of a sentence
def delete_punctuation(sentence):
    punctuation_deleter = str.maketrans('', '', string.punctuation)
    sentence = sentence.translate(punctuation_deleter)
    sentence = sentence.replace('¿', '')
    sentence = sentence.replace('¡', '')
    sentence = sentence.replace('‘', '')
    sentence = sentence.replace('’', '')
    return sentence


# Calculates the error regarding the word difficulty
def error_calculation(words_values):
    error = 0
    for x in range(0, len(words_values)):
        error += words_values[x] - WORD_DIFFICULTY

    return error / len(words_values)


# Calculates the difficult value for each word in a sentence
def calculate_sentence_words_value(root, sentence):
    word_values = []
    for j in range(0, len(sentence.words)):
        try:
            word_values.append(int(root.find(sentence.words[j].lower()).text))
        except AttributeError:
            word_values.append(0)

    return word_values


# Returns the simpler and the most challenging sentences
def better_sentences(possible_sentences):
    challenging_sentence = []
    simplest_sentence = []
    count = 0

    possible_sentences.sort(key=operator.attrgetter('difficulty'))

    while count < 3 and count < len(possible_sentences):
        challenging_sentence.append(possible_sentences[len(possible_sentences) - 1 - count])
        simplest_sentence.append(possible_sentences[count])
        count += 1

    return {"chall_sntnc": challenging_sentence, "smpl_sntnc": simplest_sentence}


def main():
    global PATH_FREQ_LIST, PATH_INPUT_WORDS, WORD, WORD_DIFFICULTY

    PATH_INPUT_WORDS = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(TITLE_SHORTED_WORDS))) + '/' + TITLE_SHORTED_WORDS

    root_input = et.parse(PATH_INPUT_WORDS).getroot()

    for word in root_input.findall('Word'):
        WORD = word.find('Word').text
        print(WORD)
        WORD_DIFFICULTY = float(word.find('WordValue').text)

        language = word.find('Language').text

        choose_language(language)

        resp = requests.get('https://linguee-api.herokuapp.com/api?q='
                            + WORD + '&src=' + INPUT_LANG + '&dst=' + OUTPUT_LANG)

        output = resp.json()

        sentences = []

        try:
            for example in output['real_examples']:
                sentences.append(clean_sentence(sentence=example['src']))
        except KeyError:
            print("Word not found in api")
            continue

        root_freg = et.parse(PATH_FREQ_LIST + TITLE_FREQ).getroot()
        possible_sentences = []

        print("\nThe word is: " + WORD + "\n")

        print("The possible sentences are:")
        for i in range(0, len(sentences)):
            sentence_words = delete_punctuation(sentences[i]).split()
            sentence = Sentence(sentences[i], sentence_words)
            sentence.add_values(calculate_sentence_words_value(root_freg, sentence))
            sentence.set_difficulty(error_calculation(sentence.words_values))

            if len(sentence.words) <= MAX_LENGTH_SENTENCE and (int(sentence.difficulty)) <= WORD_DIFFICULTY:
                possible_sentences.append(sentence)
                print(sentence)

        useful_sentences = better_sentences(possible_sentences)

        print("\nMost challenging sentences are: ")
        for x in useful_sentences["chall_sntnc"]:
            print(x)

        print("\nThe simplest sentences are: ")
        for x in useful_sentences["smpl_sntnc"]:
            print(x)


if __name__ == "__main__":
    main()
