from __future__ import division
from _collections import defaultdict
import sys

def main():
    
    emit = defaultdict(int)
    transition = defaultdict(int)
    context = defaultdict(int)
    wordToTag = dict()
    states = set()
    
    result=open('hmmmodel.txt', 'w')
    
    with open(sys.argv[1]) as f:
        for line in f:
            previous = "<s>"
            context[previous] += 1
    
            wordtags = line.strip().split(" ")
            for wordtag in wordtags:
                word = wordtag[:len(wordtag)-3]
                tag = wordtag[-2:]    
                transition[previous+" "+tag] += 1
                context[tag] += 1
                emit[tag+" "+word] += 1
                previous = tag
                
                if word not in wordToTag:
                    wordToTag[word] = set()
                    
                wordToTag[word].add(tag)  
                states.add(tag)  
            transition[previous+" </s>"] += 1
            
        
    numberOfStates = len(states)
    for key in transition:
        previous, tag = key.split(" ")
        result.write("T " + key + " " + str(transition[key])+ " " + str((transition[key] + 1)/(context[previous] + numberOfStates)) +"\n")
        
    for key in emit:
        tag, word = key.split(" ")
        result.write("E " + key + " " + str(emit[key]/ context[tag]) + "\n")
        
    for key in context:
        result.write("C " + key + " " + str(context[key]) + "\n")
    
    for key in wordToTag:
        s = "W " + key + " "
        for tag in wordToTag[key]:
            s += str(tag) + ","
        s += "\n" 
        result.write(s)
        

if __name__ == "__main__":
    main()