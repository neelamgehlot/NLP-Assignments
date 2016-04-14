from __future__ import division
from _collections import defaultdict
import sys
    

def main():
        
    emit = defaultdict(int)
    transition = defaultdict(int)
    context = defaultdict(int)
    states = set()
    start = defaultdict(int)    
    wordToTag = dict()
    
    output = open("hmmoutput.txt", 'w')
    totalStart = 0
    with open("hmmmodel.txt") as f:
        for line in f:
            if line.startswith("T"):
                temp = line.rstrip("\n").split(" ")
                transition[temp[1].strip()+" "+temp[2].strip()] = float(temp[4].strip())
                if temp[1].strip().startswith("<s>"):
                    start[str(temp[2].strip())] += int(temp[3].strip())
                    totalStart += int(temp[3].strip())
            
            elif line.startswith("E"):
                temp = line.rstrip("\n").split(" ")
                emit[temp[1].strip()+" "+temp[2].strip()] = float(temp[3].strip())
            
            elif line.startswith("C"):
                temp = line.rstrip("\n").split(" ")
                context[temp[1].strip()] = int(temp[2].strip())
                states.add(temp[1].strip())
                
            elif line.startswith("W"):
                temp = line.rstrip("\n").split(" ")
                word = temp[1].strip()
                if word not in wordToTag:
                    wordToTag[word] = set()
                tags = temp[2].strip().rstrip(",").strip()
                tags = tags.split(",")
                for tag in tags:
                    wordToTag[word].add(tag.strip())
    
    for i in states:
        start[i] = start[i] * totalStart


    with open(sys.argv[1]) as f:
        for line in f:
            obs = line.rstrip("\n").split(" ")
        
            listOfTags = viterbi(obs, states,  start, transition, emit, context, wordToTag)
            for i in range(len(listOfTags)-1, -1, -1):
                output.write(str(listOfTags[i])+" ")
            output.write("\n")
            
def viterbi(obs, states, start, transition, emit, context, wordToTag):
    v = [defaultdict(int)]
    backpointer = [defaultdict(int)]
    some_states = states
    if obs[0] in wordToTag:
        some_states = wordToTag[obs[0]]
        for i in some_states:
            if i in states and start[i] > 0 and (i+" "+obs[0].strip()) in emit:
                v[0][i] = start[i]*emit[i+" "+obs[0].strip()]
                
    else:
        for i in states:
            if i in states and start[i] > 0:
                v[0][i] = start[i]

    if "<s>" in states:
        states.remove("<s>") 

    for t in range(1, len(obs)):
        v.append(defaultdict(int))
        backpointer.append(defaultdict(int))
        some_states = states
        if obs[t] in wordToTag:
            some_states = wordToTag[obs[t]]
            
            for y in some_states:
                maxvalv = -1
                for y0 in states:
                    if((y0 in v[t-1]) and v[t-1][y0] > 0 and ((y+" "+obs[t].strip()) in emit)):
                        probvalv = v[t-1][y0]*transition[y0+" "+y]*emit[y+" "+obs[t].strip()]
                        if maxvalv <= probvalv :
                            maxvalv = probvalv
                            backpointer[t][y] = y0
                v[t][y] = maxvalv
                
        else:
            
            for y in states:
                maxvalv = -1
                for y0 in states:
                    if((y0 in v[t-1]) and v[t-1][y0] > 0):
                        probvalv = v[t-1][y0]*transition[y0+" "+y]
                        if maxvalv <= probvalv :
                            maxvalv = probvalv
                            backpointer[t][y] = y0
                v[t][y] = maxvalv
                
                
    
    listOfTags = [] 
    
    tag = ""   
    maxval = -1
    some_states = states
    if obs[len(obs) - 1] in wordToTag:
        some_states = wordToTag[obs[len(obs) - 1]]
        
    for i in some_states:
        if maxval <= v[len(obs) - 1][i]:
            maxval = v[len(obs) - 1][i]
            tag = i
    
    listOfTags.append(obs[len(obs) - 1]+"/"+tag)
                   
    for t in range(len(obs) - 2, -1, -1):
        if tag not in backpointer[t+1]:
            for i in states:
                if i in backpointer[t+1]:
                    tag = backpointer[t+1][i]
                    break;
        else:
            tag = backpointer[t+1][tag]
        listOfTags.append(obs[t]+"/"+tag)
  
    return listOfTags           
    
if __name__ == "__main__":
    main()