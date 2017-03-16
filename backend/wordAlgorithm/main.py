import algorithm
import word

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q
    
import xml.etree.cElementTree as ET

root = ET.Element("Words")


queue = algorithm.q
tempQueue = Q.PriorityQueue()
#bad print for queue used only for debugging 
#for i in range (0,queue.qsize()):
    #w = queue.get()
    #word.printWord(w[1])
    #tempQueue.put(w)

# Create reulting XML from Priority Queue
for i in range (0,queue.qsize()):
    w = queue.get()
    doc = ET.SubElement(root, "Word")
    ET.SubElement(doc,"Language").text = w[1].language
    ET.SubElement(doc,"Word").text = w[1].originalWord
    ET.SubElement(doc,"Translation").text = w[1].translatedWord
    ET.SubElement(doc,"Category").text = w[1].category
    ET.SubElement(doc,"Word_Difficulty").text = w[1].wordDifficulty
    ET.SubElement(doc,"Extensions").text = w[1].extensions
    tempQueue.put(w)
tree = ET.ElementTree(root)
tree.write("result.xml")