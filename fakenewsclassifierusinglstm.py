# -*- coding: utf-8 -*-
"""FakeNewsClassifierUsingLSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CoNxaecjcsAKwDEwNpBmvsKjVFpNTdv0

## Fake News Classifier Using LSTM
(DATASET ON KAGGLE)
"""

import pandas as pd

dataf=pd.read_csv('train.csv')

dataf.head()

dataf.shape

dataf.head()

dataf.isnull().sum()

###Drop Nan Values
dataf=dataf.dropna()

dataf.head()

## Get the Independent Features

X=dataf.drop('label',axis=1)

## Get the Dependent features
y=dataf['label']

X.shape

y.shape

import tensorflow as tf

tf.__version__

from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense

### Vocabulary size
voc_size=5000

"""### Onehot Representation"""

messages=X.copy()

messages['title'][1]

messages

#messages.reset_index(inplace=True)

messages

import nltk
import re
from nltk.corpus import stopwords

nltk.download('stopwords')

### Dataset Preprocessing
from nltk.stem.porter import PorterStemmer ##stemming purpose
ps = PorterStemmer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['title'][i])
    review = review.lower()
    review = review.split()

    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

corpus

corpus[1]

onehot_repr=[one_hot(words,voc_size)for words in corpus]
onehot_repr

corpus[1]

onehot_repr[1]

"""### Embedding Representation"""

sent_length=20
embedded_docs=pad_sequences(onehot_repr,padding='post',maxlen=sent_length)
print(embedded_docs)

embedded_docs[1]

embedded_docs[0]

## Creating model
embedding_vector_features=40 ##features representation
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(LSTM(100))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())

len(embedded_docs),y.shape



import numpy as np
X_final=np.array(embedded_docs)
y_final=np.array(y)

X_final.shape,y_final.shape

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.33, random_state=42)

"""### Model Training"""

### Finally Training
model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=10,batch_size=64)

"""### Adding Dropout"""

from tensorflow.keras.layers import Dropout
## Creating model
embedding_vector_features=40
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(Dropout(0.3))
model.add(LSTM(100))
model.add(Dropout(0.3))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

"""### Performance Metrics And Accuracy"""

y_pred=model.predict(X_test)

y_pred=np.where(y_pred > 0.6, 1,0) ##AUC ROC Curve

from sklearn.metrics import confusion_matrix

confusion_matrix(y_test,y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

