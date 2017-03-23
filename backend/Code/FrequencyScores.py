from bs4 import BeautifulSoup
import requests
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import xmltodict
import os

# Class that retrieves the score of a letter in a specified language according
# to its frequency

# Base url of the requests
BASE_URL = "http://www.sttmedia.com/"
CHARS = "characterfrequency"
SYLLABLES = "syllablefrequency"

# Select the min and max score values possible for any letter
DEF_MIN = 1
DEF_MAX = 20

# Language from which to retrieve the letter scores (as it appears
# in the web page)
LANG = "nederlands"
FOLDER = LANG + "Scores"

# This is the main function for making queries.
# An html document should be returned by the query.
def query_site(url):
    r = requests.get(url)
    print ("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return BeautifulSoup(r.text, "html.parser")
    else:
        r.raise_for_status()

# This adds a language to the url before making
# an API call to the function above.
def query_by_lang(url, lang):
    url = url + '-' + lang
    return query_site(url)

# Functions to get the max and min value of a list previously sorted
# from greater to smaller
def find_min(list):
    # Get last element of the list
    return find_value_at(list, -1)

def find_max(list):
    # Get first element of the list
    return find_value_at(list, 0)

# Returns the value at position indx of list
def find_value_at(list, indx):
    row = list[indx]
    val = row.find_all("td")[1].string[:-1]
    return float(val.replace(',', '.'))

# Maps val which is in a range of o_min to o_max to a new range between
# n_min and n_max, making o_min map to n_max and o_max to n_min
# (The higher val the smaller the new value)
def map_to_range(val, o_min, o_max, n_min, n_max):
    new_value = n_max - (val - o_min) * (n_max - n_min) / (o_max - o_min)
    return new_value

# Returns a dictionary with the letters as keys and their scores as values
def create_dict(list, min, max, MIN, MAX):
    dict = {}
    for row in list:
        tds = row.find_all("td")
        letter = tds[0].string
        freq = tds[1].string[:-1]
        freq = float(freq.replace(',', '.'))
        dict[letter] = map_to_range(freq, min, max, MIN, MAX)

    return dict

# Transforms a dictionary to a xml (a path can be specified optionally)
def dict_to_xml_file(dict, fname, path="."):
    xml = dicttoxml(dict, custom_root=fname, attr_type=False)
    dom = parseString(xml)
    with open(path + '/' + fname + ".xml", 'w') as file:
        file.write(dom.toprettyxml())

# Transforms a xml file to a dictionary (not used here but can be
# used to read the scores back to a dictionary)
def xml_file_to_dict(path, root):
    with open(path, 'r') as file:
        content = file.read()
        dict = xmltodict.parse(content)[root]
        return dict

# Option indicates whether to retrieve letter or syllable
# frequencies, table num is used for parsing reasons
def parse_frequencies(option, tableNum):
    html = query_by_lang(BASE_URL + '/' + option, LANG)
    table = html.find_all("table")[tableNum]
    list = table.find_all("tr")[2:]

    # Create the dictionary
    min = find_min(list)
    max = find_max(list)
    dict = create_dict(list, min, max, DEF_MIN, DEF_MAX)
    return dict

def retrieve_letter_frequencies():
    # Get the letter table from the page
    letterDict = parse_frequencies(CHARS, 1)
    # Print it to an xml file in a folder in the current dir
    dict_to_xml_file(letterDict, CHARS + '-' + LANG, FOLDER)

def retrieve_2letter_frequencies():
    syllableDict = parse_frequencies(SYLLABLES, 1)
    dict_to_xml_file(syllableDict, SYLLABLES + "2-" + LANG, FOLDER)

def retrieve_3letter_frequencies():
    syllableDict = parse_frequencies(SYLLABLES, 3)
    dict_to_xml_file(syllableDict, SYLLABLES + "3-" + LANG, FOLDER)

def main():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    retrieve_letter_frequencies()
    retrieve_2letter_frequencies()
    retrieve_3letter_frequencies()

if __name__ == "__main__":
    main()
