# Format of letter valuetable : [alphabetArray, languagesArray, values for each language in order array]  

letterTable = []
languages = []
letters = []
dutchValue = []
spanishValue = []

import xml.etree.ElementTree as ET
tree = ET.parse('letterValuesXML.xml');
root = tree.getroot()

for child in root:
    for child2 in child:
        if child2.tag == 'Letter':
            letters.append(child2.text)
            
        if child2.tag == 'ValueDutch':
            dutchValue.append(child2.text)
            
        if child2.tag == 'ValueSpnish':
            spanishValue.append(child2.text)
            
languages.append("Dutch")
languages.append("Spanish")

letterTable.append(letters)
letterTable.append(languages)
letterTable.append(dutchValue)
letterTable.append(spanishValue)