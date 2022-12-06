

#2 importing relevant libraries
import json
import string
import random

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
nltk.download("punkt")
nltk.download("wordnet")



data_file = open('/intents.json').read()
data = json.loads(data_file)

#4 CREATING data_X and data_Y

words = [] #for Bow model/ vocabulary for patterns. 
classes = [] #for Bow model/ vocabulary for tags
data_X = [] #for storing each pattern
data_Y = [] #for storing tag corresponding to each pattern in data_X
# Iterating over all the intents.

for intent in data["intents"]:
  for pattern in intent["patterns"]:
    tokens = nltk.word_tokenize(pattern) #tokenize each pattern
    words.extend(tokens) #and append tokens to words
    data_X.append(pattern) #appending pattern to data_X
    data_Y.append(intent["tag"]) #appending the associated tag to each pattern

  # adding the tag to the classes if it's not there already
  if intent["tag"] not in classes:
    classes.append(intent["tag"])

#initializing lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()

#lemmatize all the words in the vocab and convert them to lowercase
#if the words don't appear in punctuation

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]

#sorting the vocab and classes in alphabetical order and taking the # set
# to ensure no duplicate occur.

words = sorted(set(words))
classes = sorted(set(classes))

# making the data friendly using bag-of-words(bow) model.

#5 TEXT TO NUMBERS

training = []
out_empty = [0] * len(classes)
# creating the bag of words model
for idx, doc in enumerate(data_X):
  bow = []
  text = lemmatizer.lemmatize(doc.lower())
  for word in words:
    bow.append(1) if word in text else bow.append(0)

  # mark the index of class that the current pattern is associated to
  output_row = list(out_empty)
  output_row[classes.index(data_y[idx])] = 1
  # add the one encoded BoW and associated classes to training
  training.append([bow, output_row])

# shuffle the data and convert it to an array
random.shuffle(training)
training = np.arra(training, dtype=object)

#spit the features and target labels
train_X = np.array(list(training[:, 0]))
train_Y = np.array(list(training[:, 1]))

#6 The Neural Network Model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_X[0]),), activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_Y[0]), activation = "softmax"))
adam = tf.keras.optimizers.Adam(learning_rate = 0.01, decay = 1e-6)
model.compile(loss='categorical_crossentropy',
              optimizer = adam,
              metrics=["accuracy"])
print(model.summary())
model.fit(x=train_X, y=train_Y, epochs=150, verbose=1)

#7 preprocessing the input

def clean_text(text):
  tokens = nltk.word_tokenize(text)
  tokens = [lemmatizer.lemmatize(word) for word in tokens]
  return tokens

def bag_of_word(text, vocab):
  tokens = clean_text(text)
  bow = [0] * len(vocab)
  for w in tokens:
    for idx, word in enumerate(vocab):
      if word == w:
        bow[idx] = 1
  return np.array(bow)

def pred_class(text, vocab, labels):
  bow = bag_of_words(text, vocab)
  result = model.predict(np.array([bow]))[0] #extracting possibilities
  thresh = 0.5
  y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]
  y_pred.sort(key = lambda x: x[1], reverse = True) #Sorting by values of probability in decreasing order
  return_list = []
  for r in y_pred:
    return_list.append(labels[r[0]]) #contains labels(tags) for highest probability
  return return_list

def get_response(intents_list, intents_json):
  if len(intents_list) == 0:
    result = "Sorry! I don't understand."
  else:
    tag = intents_list[0]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
      if i["tag"] == tag:
        result = random.choice(i["responses"])
        break
  return result


# 8 Interacting with the ChatBot

print("Press 0 if you don't want to chat with our ChatBot")
while True:
  message = input("")
  if message == "0":
    break
  intents = pred_class(message, words, classes)
  result = get_response(intents, data)
  print(result)









