import requests
import xml.etree.cElementTree as et
import string

OUTPUT_LANG = 'en'

# These three values will be filled by the input when it will be implemented
INPUT_LANG = 'es'
WORD = 'cama'
WORD_DIFFICULTY = 882


TITLE = 'SpanishWordFrequencies'
PATH = "/home/antonio/Desktop/SE/FrecuencyList/" + TITLE + ".xml"
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
            word_values.append(WORD_DIFFICULTY)

    return word_values


# Returns the simpler and the most challenging sentences
def better_sentences(possible_sentences):
    challenging_sentence = ""
    simplest_sentence = ""
    min_difficulty = float("-inf")
    max_difficulty = float("inf")

    for s in possible_sentences:
        if s.difficulty > min_difficulty:
            min_difficulty = s.difficulty
            challenging_sentence = s.sentence_string

        if s.difficulty < max_difficulty:
            max_difficulty = s.difficulty
            simplest_sentence = s.sentence_string

    return {"chall_sntnc": challenging_sentence, "smpl_sntnc": simplest_sentence}


def main():
    resp = requests.get('https://linguee-api.herokuapp.com/api?q='
                        + WORD + '&src=' + INPUT_LANG + '&dst=' + OUTPUT_LANG)

    output = resp.json()

    sentences = []

    try:
        for example in output['real_examples']:
            sentences.append(clean_sentence(sentence=example['src']))
    except KeyError:
        print("Word not found in api")
        exit()

    root = et.parse(PATH).getroot()
    possible_sentences = []

    print("The possible sentences are:")
    for i in range(0, len(sentences)):
        sentence_words = delete_punctuation(sentences[i]).split()
        sentence = Sentence(sentences[i], sentence_words)
        sentence.add_values(calculate_sentence_words_value(root, sentence))
        sentence.set_difficulty(error_calculation(sentence.words_values))

        if len(sentence.words) <= MAX_LENGTH_SENTENCE and (int(sentence.difficulty)) <= WORD_DIFFICULTY:
            possible_sentences.append(sentence)
            print(sentence)

    useful_sentences = better_sentences(possible_sentences)
    print("\nThe most challenging sentence is:\n", useful_sentences["chall_sntnc"], "\nThe simplest sentence is:\n",
          useful_sentences["smpl_sntnc"])


if __name__ == "__main__":
    main()
