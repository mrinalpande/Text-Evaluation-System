# for squareroots.
import math

import pandas as pd
import computation.tfidf as tf

# for tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

# for reading all the files
from os import listdir
from os.path import isfile, join

# adding path to NLTK file
nltk.data.path = ['nltk_data']

# load stopwords
stopwords = set(stopwords.words('english'))

# path for all the training data sets
essay_train_path = 'data/train/'
essay_query_path = 'data/query/'

def get_words(message):
    all_words = set(wordpunct_tokenize(message.replace('=\\n', '').lower()))
    # remove the stopwords
    msg_words = [word for word in all_words if word not in stopwords and len(word) > 2]
    return msg_words

def get_essay_from_file(file_name):
    message = ''
    with open(file_name, 'r') as essay_file:
        for line in essay_file:
            message += line
    return message

def get_data_set(path):
    training_set = []
    essay_in_dir = [essay_file for essay_file in listdir(path) if isfile(join(path, essay_file))]

    for essay_name in essay_in_dir:
        message = get_essay_from_file(path + essay_name)
        terms = get_words(message)
        training_set.append(terms)
    
    return training_set

def compute_tfidf(data_set):
    doc_vector=[]
    wordSet={}
    tfreq=[]
    idfs=[]
    tfidf=[]
    index=0
    #This is only finding wordSet
    for terms in data_set:
        wordSet = set(wordSet).union(set(terms))
    #Initialize the vector with zeroes
    for count in range(len(data_set)):
        doc_vector.append(dict.fromkeys(wordSet,0))
    for terms in data_set:
        for word in terms:
            doc_vector[index][word]+=1
        tfreq.append(tf.computeTF(doc_vector[index],terms))
        index+=1
    idfs=tf.computeIDf(doc_vector)
    for tfs in tfreq:
        tfidf.append(tf.computeTFIDF(tfs,idfs))
    return tfidf

def compute_score(query_set,tfidf):
    doc_score=[]
    for index in range(len(tfidf)):
        score=0
        for word in query_set[0]:
            score+=tfidf[index][word]
        doc_score.append(score)
    return doc_score

def cosine_score(tfidfq,tfidfd):
    doc_cosine_score=[]
    squared_element=0
    for query in tfidfq:
        for word, val in query.items():
            squared_element+=1
    tfidfq_deno_part=math.sqrt(squared_element)
    #reset squared_element
    squared_element=0
    for query in tfidfd:
        for word, val in query.items():
            squared_element+=val*val
    tfidfd_deno_part=math.sqrt(squared_element)
    #unit vector |a||b|
    denominator=tfidfq_deno_part*tfidfd_deno_part
    doc_numerator=[]
    numerator=0
    for index in range(len(tfidfd)):
        for query in tfidfq:
            for word, val in query.items():
               numerator+=1*tfidfd[index][word]
        doc_numerator.append(numerator)
    for numerator in doc_numerator:
        doc_cosine_score.append(math.cos(math.radians(numerator/denominator)))
    return doc_cosine_score

print('Loading training sets...')
training_set=get_data_set(essay_train_path)
query_set=get_data_set(essay_query_path)
print('done.')
tfidf_training_set=compute_tfidf(training_set)
tfidf_query_set=compute_tfidf(query_set)

#Computing Score(q/d1,d2...)
doc_score= compute_score(query_set,tfidf_training_set)
print(pd.DataFrame(doc_score))