import os, string, re, sys
from _collections import defaultdict

fModel=open('nbmodel.txt', 'w')

EntireVocab=set()
VocabCount=int(0)
docCount=int(0)
PositiveTruthfulDocCount=int(0)
PositiveDeceptiveDocCount=int(0)
NegativeTruthfulDocCount=int(0)
NegativeDeceptiveDocCount=int(0)

PositiveTruthfulCount=int(0)
PositiveDeceptiveCount=int(0)
NegativeTruthfulCount=int(0)
NegativeDeceptiveCount=int(0)

PositiveTruthfulDict=defaultdict(int)
PositiveDeceptiveDict=defaultdict(int)
NegativeTruthfulDict=defaultdict(int)
NegativeDeceptiveDict=defaultdict(int)

regex = re.compile('[%s]' % re.escape(string.punctuation))

#Remove punctuation from string and check is it is valid term
def isValidTerm(s):
    if bool(s):
        s.strip()
        s=regex.sub('', s)
        if s.isalpha():
            return True, s
    return False, s

def readFile(path, label):
    with open(path, 'r') as f:
        text=f.read().replace('\n',' ');
    listOfWords=text.split()
    
    #Add words to set of entire vocabulary
    for s in listOfWords:
        valid, s=isValidTerm(s)
        if valid:
            EntireVocab.add(s)
            
    #Add words to positive truthful dictionary
    if(label=='PositiveTruthful'):
        global PositiveTruthfulCount
        for s in listOfWords:
            valid, s=isValidTerm(s)
            if valid:
                PositiveTruthfulDict[s]+=1
                PositiveTruthfulCount+=1
    
    #Add words to positive deceptive dictionary
    elif(label=='PositiveDeceptive'):
        global PositiveDeceptiveCount
        for s in listOfWords:
            valid, s=isValidTerm(s)
            if valid:
                PositiveDeceptiveDict[s]+=1
                PositiveDeceptiveCount+=1
                    
    #Add words to negative truthful dictionary
    elif(label=='NegativeTruthful'):
        global NegativeTruthfulCount
        for s in listOfWords:
            valid, s=isValidTerm(s)
            if valid:
                NegativeTruthfulDict[s]+=1
                NegativeTruthfulCount+=1
                    
    #Add words to negative deceptive dictionary
    elif(label=='NegativeDeceptive'):
        global NegativeDeceptiveCount
        for s in listOfWords:
            valid, s=isValidTerm(s)
            if valid:
                NegativeDeceptiveDict[s]+=1
                NegativeDeceptiveCount+=1
        
#Get all files
for root, directories, filenames in os.walk(sys.argv[1]): 
    for filename in filenames: 
        name=str(os.path.join(root,filename))
        if('README' not in name.upper() and name.endswith(".txt")):
            docCount+=1
            if('positive' in name.lower()):
                if('truthful' in name.lower()):
                    readFile(name, 'PositiveTruthful')
                    PositiveTruthfulDocCount+=1
                elif('deceptive' in name.lower()):
                    readFile(name, 'PositiveDeceptive')
                    PositiveDeceptiveDocCount+=1
            elif('negative' in name.lower()):
                if('truthful' in name.lower()):
                    readFile(name, 'NegativeTruthful')
                    NegativeTruthfulDocCount+=1
                elif('deceptive' in name.lower()):
                    readFile(name, 'NegativeDeceptive')
                    NegativeDeceptiveDocCount+=1
 
Classes={'PositiveTruthful': (PositiveTruthfulDocCount, PositiveTruthfulDict, PositiveTruthfulCount),
         'PositiveDeceptive': (PositiveDeceptiveDocCount, PositiveDeceptiveDict, PositiveDeceptiveCount),
         'NegativeTruthful': (NegativeTruthfulDocCount, NegativeTruthfulDict, NegativeTruthfulCount),
         'NegativeDeceptive': (NegativeDeceptiveDocCount, NegativeDeceptiveDict, NegativeDeceptiveCount)
         }    

VocabCount=len(EntireVocab)

#Compute conditional probability of each term
for ClassName in Classes:
    Count, Dict, wordCount=Classes[ClassName]
    for word in EntireVocab:
        if bool(word):
            if word in Dict:
                temp=(Dict[word]+1)/float(wordCount+VocabCount)
            else:
                temp=(1)/float(wordCount+VocabCount)
            fModel.write(ClassName+" "+word+" "+str(temp)+"\n")
        
    
