#!/usr/bin/python3
from keras.models import load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence

def no_filter():
    f = '\t\n'
    return f

def one_hot(text, n, filters, lower = True, split = " "):
    sequence = text_to_word_sequence(text, filters, lower, split)
    bytes_seq = []
    for x in sequence:
        bytes_seq.append(x.encode('utf-8'))
    int_seq = []
    for x in bytes_seq:
        int_seq.append(int.from_bytes(x, byteorder='big') % n)
    return int_seq

def no_of_words_in_data(x_train):
    word_set = set()
    for row in x_train:
        for word in row.split(' '):
            word_set.add(word)
    return len(word_set)

def load_dataset(path, interp = True):
    x_train = []
    y_train = []
    post = '.txt'
    if not interp:
        post = '_no_interp.txt'

    f = open(path+'sentences'+post, 'r')
    for line in f:
        x_train.append(line.rstrip('\n'))
    f.close()
    f = open(path+'pos'+post, 'r')
    for line in f:
        y_train.append(line.rstrip('\n').split(' '))
    f.close()
    return x_train, y_train

x_train, y_train = load_dataset('../data/korpus/train/', interp = True)
num_words = 92891

model = load_model('test2.h5')
wocab = [
            'Adjective',
            'Numeral',
            'Adverb',
            'Interjection',
            'Conjunction',
            'Noun',
            'Pronoun',
            'Verb',
            'Preposition',
            'Particle',
            'Unknown, Not Determined, Unclassifiable',
            'Punctuation (also used for the Sentence Boundary token)'
         ]
x = range(1,13)
y = ['0','A','C','D','I','J','N','P','V','R','T','X','Z']
map = dict(zip(x, wocab))
#sentence = input("Wpisz_zdanie\n")
sentence = " konie z Krępy , odchodził o siódmej z minutami  "

x = one_hot(sentence, num_words, filters = no_filter())
print(x)
## = len(x)
x = [x]
x = sequence.pad_sequences(x, 10)
#print(sentence)
print(x)

#y = x

predictions =  model.predict(x)

predicted_idx = []
for sent in predictions:
    for word in range(0,len(sent)):#len(sent)-x_len,len(sent)):
        print (word)
        idx = sent[word].tolist().index(max(sent[word]))
        predicted_idx.append(idx)
        print (sent[word])

print(sentence)
print (predicted_idx)
for i in predicted_idx:
    print (str(i) + " " + map[i])
