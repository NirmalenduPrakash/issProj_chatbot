
import numpy as np
import nltk
import random
import string,json
from os.path import abspath, exists
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Hawker:
    def __init__(self):
        self.jsondata=json.load(open('data.json'))
        self.preprocess(self.jsondata)
        self.TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
    def preprocess(self,jsondata):
        self.sent_tokens=[]
        for j in self.jsondata:
            for key,value in j.items():
                self.sent_tokens.append(value)
        self.word_tokens = nltk.word_tokenize(','.join(self.sent_tokens))
        self.lemmer = nltk.stem.WordNetLemmatizer()
    def LemTokens(self,tokens):
        return [self.lemmer.lemmatize(token) for token in tokens] 
    def LemNormalize(self,text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    def getHawkersbyLocation(self,location):
        actualNames=[]
        # for hawker in hawkerNames:
        for hc in self.jsondata:
            sent_tokens=[]
            for key,value in hc.items():
                if(key=='DESCRIPTION_MYENV'):
                    sent_tokens.extend(nltk.sent_tokenize(value))
                else:
                    sent_tokens.append(value)  
            sent_tokens.append(location)        
            # TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
            tfidf = self.TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx=vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]   
            if req_tfidf!=0:                    
                actualNames.append(hc['NAME'])
            if(len(actualNames)>4):
                break    
        return actualNames

    def getHawkerDetails(self,hawker_name,key):
        # actualName=self.filterHawkerNames([hawker_name])[0]
        hawker_details=[hc for hc in self.jsondata if hc['NAME']==hawker_name][0]
        if(key in hawker_details):
            return hawker_details[key]
        else:
            return -1
    def getHawkerDetailsFromDescription(self,hawker_name,key):
        HCs=[hc for hc in self.jsondata if hawker_name.lower() in hc['NAME'].lower()]
        for hc in HCs:
            sent_tokens=nltk.sent_tokenize(hc['DESCRIPTION_MYENV'])  
            sent_tokens.append(key)           
            # TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
            tfidf = self.TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx=vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]              
            if req_tfidf!=0:
                return sent_tokens[idx]
            else:
                continue
        return -1    
    def searchHawker(self,query):
        result=[]
        for hc in self.jsondata:
            sent_tokens=[]
            for key,value in hc.items():
                sent_tokens.append(value)
            sent_tokens.append(query)

            # TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
            tfidf = self.TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx=vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]   
            if req_tfidf!=0:
                result.append({'score':req_tfidf,'name':hc['NAME'],'sent':sent_tokens[idx]}) 
        if(len(result)!=0):        
            maxIndx=np.argmax(np.array([r['score'] for r in result]))
            return {'name':result[maxIndx]['name'],'sent':result[maxIndx]['sent']}   
        else:
            return -1     
        




