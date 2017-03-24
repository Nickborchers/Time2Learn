from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
import csv
import xml.etree.cElementTree as ET

"""Files module

This module contains all functions related with reading from or writing to files.

"""

def dict_to_xml_file(dict, file_name, path='.'):
    """Transforms a dictionary to a xml file

    :param dict:        -- the dictionary to transform
    :param file_name:   -- string with the name of the xml file
    :param path:        -- string with the path where to create the xml file (default current path)

    """
    xml = dicttoxml(dict, custom_root=file_name, attr_type=False)
    dom = parseString(xml)
    with open(path + '/' + file_name + ".xml", 'w') as file:
        file.write(dom.toprettyxml())

#
def xml_file_to_dict(path, root):
    """Transforms a xml file to a dictionary

    :param path:        -- string with the path to the xml file
    :param root:        -- string with the root tag name of the xml file
    :return:            -- a dictionary with the data of the xml file

    """
    with open(path, 'r') as file:
        content = file.read()
        return xmltodict.parse(content)[root]


def csv_file_to_dict(path):
    """Transforms a csv file to a dictionary

    :param path:        -- string with the path to the csv file
    :return:            -- a dictionary with the data of the csv file

    """
    with open(path, 'r') as file:
        reader = csv.reader(file)
        d = {}
        for row in reader:
            freq, word = row
            d[word] = freq

        return d

def xml_file_to_list(path):
    """Transforms a xml file to a list

    :param path:        -- string with the path to the xml file
    :return:            -- list with the contents of the xml file

    """
    with open(path, 'r') as file:
        tree = ET.ElementTree(file=file)
        return tree.getroot()[0]