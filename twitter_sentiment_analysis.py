# -*- coding: utf-8 -*-
"""Twitter_Sentiment_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aP_M0gAIB8--lDjf6d_wgOWWIXFblTgH
"""

!pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# importing dataset
# api fetch from kaggle
!kaggle datasets download -d kazanova/sentiment140

# extracting compressed dataset

from zipfile import ZipFile
dataset='/content/sentiment140.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('the dataset is extracted')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn .feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

print(stopwords.words('english'))

"""Data processing"""

# loading data from csv from pandas

twitter_data=pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding='ISO-8859-1')

twitter_data.head()

twitter_data.shape

# naming the column and read dataset again

column_names=['target','id','date','flag','user','text']
twitter_data=pd.read_csv('/content/training.1600000.processed.noemoticon.csv',names=column_names,encoding='ISO-8859-1')

twitter_data.head()

twitter_data.shape

twitter_data['target'].value_counts()

twitter_data.info()

twitter_data.isnull().sum()

"""convert the target 4 to 1"""

twitter_data.replace({'target':{4:1}},inplace=True)

twitter_data.head()

twitter_data['target'].value_counts()

# 0-negative tweet
# 1-positive tweet

"""STEMMING"""

port_stem=PorterStemmer()

def stemming(content):

  stemmed_content=re.sub('[^a-zA-Z]',' ',content)
  stemmed_content=stemmed_content.lower()
  stemmed_content=stemmed_content.split()
  stemmed_content=[port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content=' '.join(stemmed_content)

  return stemmed_content

twitter_data['stemmed_content']=twitter_data['text'].apply(stemming)

X=twitter_data['stemmed_content'].values
Y=twitter_data['target'].values

print(X)
print(Y)

# slitting ito train and test data
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

print(X_test.shape)
print(X_train.shape)

# converting txt inti vector

vectorizer=TfidfVectorizer()

X_train=vectorizer.fit_transform(X_train)
X_test=vectorizer.transform(X_test)

print(X_train)

print(X_test)

# traininh ml model

model=LogisticRegression(max_iter=1000)

model.fit(X_train ,Y_train)

# model evalution

X_train_predition=model.predict(X_train)
training_data_accuracy=accuracy_score(Y_train,X_train_predition)

print('accuracy_score on training data:',training_data_accuracy)

X_test_predition=model.predict(X_test)
test_data_accuracy=accuracy_score(Y_test,X_test_predition)

print(test_data_accuracy)

import pickle

filename='sentiment_analysis_model.sav'
pickle.dump(model,open(filename,'wb'))

# loading saved model

loaded_model=pickle.load(open('sentiment_analysis_model.sav','rb'))

X_new=X_test[200]
print(Y_test[200])
prediction=loaded_model.predict(X_new)
print(prediction)



if prediction[0]==0:
  print('negative tweet')
else:
  print("positive tweet")

X_new=X_test[2]
print(Y_test[2])
prediction=loaded_model.predict(X_new)
print(prediction)



if prediction[0]==0:
  print('negative tweet')
else:
  print("positive tweet")

