import math, os, sys, operator, string, re

regex = re.compile('[%s]' % re.escape(string.punctuation))

PositiveTruthfulDict=dict()
PositiveDeceptiveDict=dict()
NegativeTruthfulDict=dict()
NegativeDeceptiveDict=dict()
EntireVocab=set()

Classes=['PositiveTruthful', 'PositiveDeceptive', 'NegativeTruthful', 'NegativeDeceptive']
CondProbability={'PositiveTruthful' : PositiveTruthfulDict, 
                 'PositiveDeceptive' : PositiveDeceptiveDict, 
                 'NegativeTruthful' : NegativeTruthfulDict, 
                 'NegativeDeceptive' : NegativeDeceptiveDict
                }

fout=open('nboutput.txt','w')

#Read Naive Bayes Model generated from training data
with open('nbmodel.txt', 'r') as fModel:
    lines=fModel.readlines()
    for line in lines:
        ClassName, word, condProb =line.split()
        ClassName=ClassName.strip()
        word=word.strip()
        CondProbability[ClassName][word]=float(condProb)
        EntireVocab.add(word)   
 
#Classify each file     
for root, directories, filenames in os.walk(sys.argv[1]):
    for filename in filenames: 
        name=str(os.path.join(root,filename))
        if('README' not in name.upper() and name.endswith(".txt")):
            score={'PositiveTruthful' :float(0.0), 'PositiveDeceptive':float(0.0), 'NegativeTruthful':float(0.0), 'NegativeDeceptive':float(0.0)}
            with open(name, 'r') as f:
                text=f.read().replace('\n',' ');
            listOfWords=text.split()
            for word in listOfWords:
                if bool(word):
                    word=word.strip()
                    word=regex.sub('', word)
                    if word.isalpha() and word in EntireVocab:
                        for c in Classes:
                            score[c]+=math.log(CondProbability[c][word])    
            ClassName=max(score.iteritems(), key=operator.itemgetter(1))[0]
            if(ClassName=='PositiveTruthful'):
                fout.write('truthful positive '+name+"\n")
            elif(ClassName=='PositiveDeceptive'):
                fout.write('deceptive positive '+name+"\n")
            elif(ClassName=='NegativeTruthful'):
                fout.write('truthful negative '+name+"\n")
            elif(ClassName=='NegativeDeceptive'):
                fout.write('deceptive negative '+name+"\n")


