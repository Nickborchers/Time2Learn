from query import query_site
from files import xml_file_to_list, dict_to_xml_file
from collections import defaultdict

"""

Class that calls a translation API to translate words and stores the
translations as an xml file

"""

GLOSBE = 0
LINGUEE = 1

LANG = "Spanish"
FROM = "es"
DEST = "en"

# Path of the xml file with the words
PATH = "/Users/PhoenixQoH/Desktop/Words/"

# Glosbe API parameters
BASE_GLOSBE_URL = "https://glosbe.com/gapi/translate"

# Linguee API parameters
BASE_LINGUEE_URL = "https://linguee-api.herokuapp.com/api"

def query_glosbe_by_word(url, word, from_lang, dest_lang, fmt="json"):
    """Queries the Glosbe API for the translations of a word

    :param url:         -- string with base Glosbe url
    :param word:        -- string with the word to translate
    :param from_lang:   -- string with the iso code of the language of the word
    :param dest_lang:   -- string with the iso code of the language to which to translate the word
    :param fmt:         -- string with the format in which to receive the query response (default JSON)
    :return:            -- a json object with the query response

    """
    params = {}
    params["pretty"] = "true"
    params["from"] = from_lang
    params["dest"] = dest_lang
    params["phrase"] = word
    params["format"] = fmt
    return query_site(url, params)

def query_linguee_by_word(url, word, from_lang, dest_lang):
    """Queries the Linguee API for the translations of a word

    :param url:         -- string with base Linguee url
    :param word:        -- string with the word to translate
    :param from_lang:   -- string with the iso code of the language of the word
    :param dest_lang:   -- string with the iso code of the language to which to translate the word
    :return:            -- a json object with the query response

    """
    params = {}
    params["q"] = word
    params["src"] = from_lang
    params["dst"] = dest_lang
    return query_site(url, params)


def parse_linguee_result(input):
    """Gets the word translations from a json object and stores them in a list

    :param input:       -- json object with the response of the Linguee API
    :return:            -- list with all the word translations
    """
    list = []
    result = input["exact_matches"]
    if result == []:
        return []

    result = result[0]["translations"]
    for res in result:
        list.append(res["text"])

    return list

def parse_glosbe_result(input):
    """Gets the word translations from a json object and stores them in a list

    :param input:       -- json object with the response of the Glosbe API
    :return:            -- list with all the word translations

    """
    list = []
    result = input["tuc"]

    for res in result:
        if "phrase" in res:
            res = res["phrase"]
            if res["language"] == DEST:
                list.append(res["text"])

    return list

def translate(word, from_lang, dest_lang, api):
    """Gets all words translations from an API and stores them in a list

    :param word:        -- string with the word
    :param from_lang:   -- string with the language of the word
    :param dest_lang:   -- string with the language to which translate the word
    :param api:         -- int with the API to use
    :return:            -- list with all posibble translations of the word

    """
    return {
        GLOSBE: parse_glosbe_result(query_glosbe_by_word(BASE_GLOSBE_URL, word, from_lang, dest_lang)),
        LINGUEE: parse_linguee_result(query_linguee_by_word(BASE_LINGUEE_URL, word, from_lang, dest_lang))
    }[api]

def main():
    words = xml_file_to_list(PATH + LANG + ".xml")

    d = defaultdict(list)

    for w in words:
        # Remove adjective terminations
        indx = w.text.find(',')
        if (indx != -1):
            w.text = w.text[:indx]

        # Store the meanings in a dictionary
        # Change the method call to use either Glosbe or Linguee API
        meanings = translate(w.text, FROM, DEST, GLOSBE)

        d[w.text] = meanings

    dict_to_xml_file(d, LANG + "-English")

if __name__ == "__main__":
    main()
