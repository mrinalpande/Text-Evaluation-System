import csv
from distutils.util import strtobool
from sklearn.naive_bayes import GaussianNB as GNB
import numpy as np
import pandas as pd
import os
import random

#check for limits
def check(inc, cor):
    list1=['qwertyuiop','asdfghjkl','zxcvbnm']
    i=0
    j=0
    while i<3:
        while j<len(list1[i]):
            if cor == list1[i][j]:
                if first_last(cor)==1:
                    if inc==list1[i][j+1]:
                        return 1
                elif first_last(cor)==2:
                    if inc==list1[i][j-1]:
                        return 1
                else:
                    if inc==list1[i][j-1] or inc==list1[i][j+1]:
                        return 1
            j+=1
        j=0
        i+=1
    return 3

#Defining first and last limits
def first_last(cor):
    list1=["qaz","plm"]
    for j in range(3):
        if cor==list1[0][j]:
            return 1
        elif cor==list1[1][j]:
            return 2
    return 0

#creating and initializing a newfile
def create_newfile(file):
    initialize=['acceptance','encoding','word']
    with open(file,'w') as new_file:
        writer=csv.writer(new_file)
        writer.writerow(initialize)
    new_file.close()

# append mode
def append(file,words):
    with open(file,'a') as file_append:
        writer=csv.writer(file_append)
        writer.writerow(words)
    file_append.close()
    
# Read mode
def read(file):
    df =pd.read_csv(file,converters={'encoding':str})
    acceptance=[word for word in df['acceptance']]
    encoding=[word for word in df['encoding']]
    #converting encodings back to list of integers    
    list_encoding=[]
    K=[]
    for word in encoding:
        for integers in word:
            K.append(int(integers))
        list_encoding.append(K)
        K=[]
    dataset={'acceptance':acceptance,'encoding':list_encoding}    
    return dataset 

#generates filename according to the entered word
def filename_gen(word):
    filename=str(len(word))+'_word.csv'
    if os.path.isfile(filename):
        return filename
    else:
        #generate a new file
        create_newfile(filename)
        return filename

# Does the encoding on the basis of correct word
def encoding(entered_word,correct_word):
    j=0
    encoded_list=[]
    while j<len(correct_word):
        if entered_word[j]==correct_word[j]:
            encoded_list.append(0)
        elif j<len(correct_word)-1:               
            if entered_word[j]==correct_word[j+1] and entered_word[j+1]==correct_word[j]:
                encoded_list.append(2)
                encoded_list.append(2)
                j+=1
            else:
                encoded_list.append(check(entered_word[j],correct_word[j]))
        else:
            encoded_list.append(check(entered_word[j],correct_word[j]))
        j+=1
    number=int()
    for letter in encoded_list:
        number=str(number)+str(letter) if number!=0 else str(letter)
    return number

#Take Inputs for Training Data.
def inputs():
    i=0
    words=[]
    correct_word=input("Enter the correct word: ")
    words=[1,str(encoding(correct_word,correct_word)),correct_word]
    filename=filename_gen(correct_word)
    append(filename,words)
    print("Enter 10 correct data sets for training data: \n")
    while i<10:
        entered_word=input("Enter word:")
        words=[1,str(encoding(correct_word,entered_word)),entered_word]
        append(filename,words)
        i+=1
    i=0
    print("Enter 10 incorrect data sets for training data: \n")
    while i<10:
        entered_word=input("Enter word:")
        words=[0,str(encoding(correct_word,entered_word)),entered_word]
        append(filename,words)
        i+=1        

#scoring
def score(encoding):
    length=len(encoding)
    per_letter=1.0/length
    final_score=0.0    
    score_look_up_table={0:per_letter,1:(per_letter*.5),2:(per_letter*.75),3:0}
    for encoded_letter in encoding:
        for i in range(4):
            if encoded_letter==i:
                final_score+=score_look_up_table[i]
    return final_score

#Loading Q&A
def load_QA():
    df=pd.read_csv('Q&A.csv')
    question=[ques for ques in df['question']]
    answer=[ans for ans in df['answer']]
    dataset={'question':question,'answer':answer}
    return dataset
#Comprehending all functions    
def main():
    arr=strtobool(input('Do you want to append a new word in our training data set?\n'))
    if arr:
        inputs()
        print("Appended Successfully")
    print("Welcome to dumb Q&A's.")
    #Loading Q&A
    ques_ans=load_QA()
    for index in range(len(ques_ans['question'])):
        print(ques_ans['question'][index])
        correct_word=ques_ans['answer'][index]
        check_word=input('Enter you answer :')
        print('checking acceptability on the basis of training data set...\n')
        print('Loading Dataset.\n')
        #loading Dataset
        dataset=read(filename_gen(correct_word))
        #print(dataset['acceptance'])
        #print(dataset['encoding'])
        print('Dataset successfully loaded!!!')
        encode_check_word=encoding(check_word,correct_word)
        encode_check_word=[int(word) for word in str(encode_check_word)]
        x = np.array(dataset['encoding'])
        y = np.array(dataset['acceptance'])
    
        model = GNB()

        model.fit(x,y)
    
        predicted= model.predict([encode_check_word])
        print (predicted)
        if all(predicted):
            print("answer is accepted")
        else:
            print("answer is not accepted")
        print("Score is :",score(encode_check_word))
main()
