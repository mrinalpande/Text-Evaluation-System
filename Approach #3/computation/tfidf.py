#tfidf teaching computer to read
#my,on,sat,the common words
#tfidf better stratergy to count
#tdidf score to rank the importance
# tfidf=termfrequency*inverse frequency
# termfrequency = 1 + log(number of times a word appears) 
# inverse doc frequency = log(number of docs/number of docs containing word)
import math

#Computing TF
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        if count > 0:
            tfDict[word] = 1 + math.log(count)
        else:
            tfDict[word] = 0
    return tfDict

#Computing IDF
def computeIDf(doclist):
    idfDict = {}
    N = len(doclist)
    idfDict = dict.fromkeys(doclist[0].keys(), 0)
    for doc in doclist:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] +=1
            
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

#Computing TFIDF
def computeTFIDF(tfbow,idfs):
    tfidf = {}
    for word,val in tfbow.items():
        tfidf[word] = val* idfs[word]
    return tfidf
