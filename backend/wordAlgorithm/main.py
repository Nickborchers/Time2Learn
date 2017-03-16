import algorithm
import word

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q


queue = algorithm.q
tempQueue = Q.PriorityQueue()
#bad print for queue used only for debugging 
for i in range (0,queue.qsize()):
    w = queue.get()
    word.printWord(w[1])
    tempQueue.put(w)