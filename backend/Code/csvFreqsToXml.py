import csv
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

# Class that transforms a csv file containing the frequencies of each word
# to an xml file

CSV_PATH = "/Users/PhoenixQoH/Desktop/"
LANG = "Dutch"

# Transforms a dictionary to a xml (a path can be specified optionally)
def dict_to_xml_file(dict, fname, path="."):
    xml = dicttoxml(dict, custom_root=fname, attr_type=False)
    dom = parseString(xml)
    with open(path + '/' + fname + ".xml", 'w+') as file:
        file.write(dom.toprettyxml())

def main():
    reader = csv.reader(open(CSV_PATH + "freq" + LANG + ".csv", 'r'))
    d = {}
    for row in reader:
        v, k = row
        d[k] = v

    dict_to_xml_file(d, LANG + "WordFrequencies")

if __name__ == "__main__":
    main()