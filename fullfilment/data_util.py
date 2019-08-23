#!/usr/bin/env python
# coding: utf-8

# In[10]:


import re
import json
import nltk
import string
import numpy as np
from os.path import abspath, exists
#nltk.download()
from nltk.corpus import stopwords 
################################
################################
##########INPUT TESTING################
input="find chicken noodles"
##############################
#############################
############################
input="elder seating"
######################
input="car parking"
###################
input="near mrt"
#############################


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
stop_words = set(stopwords.words('english')) 
print("here")
a=[]
b=[]
c=[]
l=[]


with open(abspath("data.json"), mode="r", encoding="UTF-8") as json_file:
            data_objs = json.loads(json_file.readlines())
hawker_objs = data_objs
score=[]
i=0
for hawker_item in hawker_objs["Hawker List"]:
            a.append([])
            b.append([])
            c.append([hawker_item["NAME"]])
            score.append([])
            y=""
            x=hawker_item["DESCRIPTION"]
            if("DESCRIPTION_MYENV" in hawker_item):
                y = hawker_item["DESCRIPTION_MYENV"]
            z=x+ " \n"+y+" \n"
            sent_tokens = [token for token in re.split('\n|,|[.]',z) if token != ""]
            j=0
               
            for stoken in sent_tokens:
                    score[i].append(0)
                    b[i].append(stoken)
                    t= nltk.word_tokenize(stoken.lower().translate(remove_punct_dict))
                    a[i].append([])
                    
                    
                    
                    for wtoken in t:
                        if not wtoken in stop_words:
                            a[i][j].append(wtoken.lower())
                            
                            
                        
                   
                    j=j+1
            i=i+1
                    

#print(score) 
#print(score[0][2])

q=[]
t= nltk.word_tokenize(input)
for wtoken in t:
                        if not wtoken in stop_words:
                            q.append(wtoken.lower())
qwe=0          
#print(a)
i=0
max_i=0
max_j=0
max_score=0
#print(q)
for l1 in a:
    j=0
    for l2 in l1:
        k=0
        score_index=[]
        for l3 in l2:
            
            #print(l3)
           # print(len(a),len(l1),len(l2),len(l3))
            for wtoken in q:
                #print(wtoken)
                #print(score[i][j])
                if(wtoken==l3):
                   # print(score[i][j])
                   
                    score[i][j]=score[i][j]+1
                    #print(wtoken)
                   
                    score_index.append(k)
                    continue
                   
                    
            #print(score[i][j])     
            k=k+1
        if ( score_index!=[]):
            #print("hello")
            score[i][j]=score[i][j]-np.var(score_index)/50
        if(score[i][j]>max_score):
            max_score=score[i][j]
            max_i=i
            max_j=j
          
        j=j+1
    i=i+1
    
#print(score)
print(max_score)
print(max_i)
print(max_j)
print(b[max_i][max_j])
print(c[max_i])
                    
                    

                    
                
            #l.append(x+ " \n"+y+" \n")
#file2 = open("C:/Users/abhin/Downloads/myfile2.txt","w")    
#file2.writelines(l) 
#file2.close()
            
        
#f=open('C:/Users/abhin/Downloads/myfile2.txt','r')
        
        #print("here 6")
        #print(len(self.raw))
#raw=f.read()# converts to lowercase
#raw=raw.lower()
#print(raw)
#self.word_tokens = nltk.word_tokenize(self.raw)
        
#sent_tokens = [token for token in re.split('\n|,|[.]',raw) if token != ""]
#word_tokens = nltk.word_tokenize(sent_tokens)
#print(sent_tokens)
#p=[]
#for stoken in sent_tokens:
    #print(stoken)
    #if(stoken!=''):
       # p.append(stoken)
    
#print(p)


# In[ ]:




