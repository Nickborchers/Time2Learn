import requests
import xml.etree.cElementTree as ET
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from collections import defaultdict

# Class that calls a translation API to translate words and stores the
# translations as an xml file

LANG = "Spanish"
FROM = "es"
DEST = "en"

# Path of the xml file with the words
PATH = "/Users/PhoenixQoH/Desktop/Words/"

# Glosbe API parameters
BASE_GLOSBE_URL = "https://glosbe.com/gapi/translate"
gparams = {}
gparams["pretty"] = "true"
gparams["from"] = FROM
gparams["dest"] = DEST

# Linguee API parameters
BASE_LINGUEE_URL = "https://linguee-api.herokuapp.com/api"
lparams = {}
lparams["src"] = FROM
lparams["dst"] = DEST

# This is the main function for making queries to the translation API.
# A json document should be returned by the query.
def query_site(url, params):

    r = requests.get(url, params=params)
    #print ("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()

# This adds a word to the query parameters before making
# an API call to the function above.
def query_glosbe_by_word(url, params, word, fmt="json"):
    params["phrase"] = word
    params["format"] = fmt
    return query_site(url, params)

# This adds a word to the query parameters before making
# an API call to the function above.
def query_linguee_by_word(url, params, word):
    params["q"] = word
    return query_site(url, params)

# Store all returned translations by Linguee in a list
def parse_linguee_result(input):
    list = []
    result = input["exact_matches"]
    if result == []:
        return []

    result = result[0]["translations"]
    for res in result:
        list.append(res["text"])

    return list

# Store all returned translations by Glosbe in a list
def parse_glosbe_result(input):
    list = []
    result = input["tuc"]

    for res in result:
        if "phrase" in res:
            res = res["phrase"]
            if res["language"] == DEST:
                list.append(res["text"])

    return list

def query_glosbe(word):
    result = query_glosbe_by_word(BASE_GLOSBE_URL, gparams, word)
    meanings = parse_glosbe_result(result)

    return meanings

def query_linguee(word):
    result = query_linguee_by_word(BASE_LINGUEE_URL, lparams, word)
    meanings = parse_linguee_result(result)

    return meanings

# Transforms a dictionary to a xml (a path can be specified optionally)
def dict_to_xml_file(dict, fname, path="."):
    xml = dicttoxml(dict, custom_root=fname, attr_type=False)
    dom = parseString(xml)
    with open(path + '/' + fname + ".xml", 'w') as file:
        file.write(dom.toprettyxml())

def main():
    # Read the words from an xml file
    tree = ET.ElementTree(file=PATH + LANG + ".xml")
    root = tree.getroot()
    words = root[0]

    d = defaultdict(list)

    for w in words:
        # Remove adjective terminations
        indx = w.text.find(',')
        if (indx != -1):
            w.text = w.text[:indx]

        # Store the meanings in a dictionary
        # Change the method call to use either Glosbe or Linguee APIS
        meanings = query_glosbe(w.text)
        #meanings = query_linguee(w.text)

        d[w.text] = meanings

    dict_to_xml_file(d, LANG + "-English")

if __name__ == "__main__":
    main()
