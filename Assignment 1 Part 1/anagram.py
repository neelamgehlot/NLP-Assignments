
def swapCharacters(l, index1, index2):
    temp=l[index1]
    l[index1]=l[index2]
    l[index2]=temp
    return l

anagramList=list()
f=open("anagram_out.txt","w")

def getAnagram(l, start, end):
    if(start==end):
        anagramList.append(''.join(l))
    else:
        for i in range(start, end+1):
            swapCharacters(l, start, i)
            getAnagram(l, start+1, end)
            swapCharacters(l, start, i)            
    
    
string = raw_input()
l=list(string)
start=int(0)
end=len(string)-1

getAnagram(l, start, end)
anagramList.sort()

for i in range(0,len(anagramList)):
    f.write(anagramList[i]+"\n")