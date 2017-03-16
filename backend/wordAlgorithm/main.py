import algorithm
import word

queue = algorithm.q

for i in range (0,queue.qsize()):
    w = queue.get()
    word.printWord(w[1])