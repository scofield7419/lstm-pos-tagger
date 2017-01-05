#!/usr/bin/python3

### IMPORT SECTION ###
import numpy as np

from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Input, Merge, merge, ChainCRF
from keras.layers.wrappers import TimeDistributed, Bidirectional
from keras.models import Model, Sequential
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence, base_filter
from keras.utils import np_utils

### end of IMPORT SECTION ###

### METHODS SECTION ###

def no_filter():
    f = '\t\n'
    return f

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

def no_of_words_in_data(x_train):
    word_set = set()
    for row in x_train:
        for word in row.split(' '):
            word_set.add(word)
    return len(word_set)

def one_hot(text, n, filters, lower = True, split = " "):
    sequence = text_to_word_sequence(text, filters, lower, split)
    bytes_seq = []
    for x in sequence:
        bytes_seq.append(x.encode('utf-8'))
    int_seq = []
    for x in bytes_seq:
        int_seq.append(int.from_bytes(x, byteorder='big') % n)
    return int_seq

def convert_word_to_int(x_train, num_words, interp = True):
    x = []
    fun = None
    if interp:
        fun = no_filter()
    else:
        fun = base_filter()
    for row in x_train:
        x.append(one_hot(row, num_words, filters = fun))
    return x


def convert_dataset_to_int(x_train, y_train, num_words, interp = True):
    return convert_word_to_int(x_train, num_words, interp), y_train

### end of METHODS SECTION ###

### DATASET SECTION ###
#x_train = [[1]] #TO DO - load sentences
#y_train = [[1]] #TO DO - load PoSes
x_train, y_train = load_dataset("../data/korpus/training/", interp = True)
x_test, y_test = load_dataset("../data/korpus/test/", interp = True)
x_val, y_val = load_dataset("../data/korpus/validation/", interp = True)


#num_words = 100 #TO DO - number of different words in dataset
num_words = no_of_words_in_data(x_train)
num_words = num_words *3
print ('num_of_word = ' + str(num_words))

x_train, y_train = convert_dataset_to_int(x_train, y_train, num_words, interp = True)
x_test, y_test = convert_dataset_to_int(x_test, y_test, num_words, interp = True)
x_val, y_val = convert_dataset_to_int(x_val, y_val, num_words, interp = True)

num_features = 32 #TO DO - how to know how much features we need. Hardcoded 3 for present time.
seq_length = max([len(s) for s in x_train]) #maximum length of sentence
print("Seq Length: " + str(seq_length))
#print('DEBUG#seq_length:',seq_length)

max_cat = 12 #out tagset have 12 categories for PoS and PoS = 0 for "no word", but that will be add at code
no_cat = max_cat
#no_cat = set([ys for sent in y_train for ys in sent])
#no_cat = min(len(no_cat), max_cat) #number of PoS categories in DataSet
#print('DEBUG#no_cat:',no_cat)

x_train = sequence.pad_sequences(x_train, maxlen = seq_length)
y_train = sequence.pad_sequences(y_train, maxlen = seq_length)
x_test = sequence.pad_sequences(x_test, maxlen = seq_length)
y_test = sequence.pad_sequences(y_test, maxlen = seq_length)
x_val = sequence.pad_sequences(x_val, maxlen = seq_length)
y_val = sequence.pad_sequences(y_val, maxlen = seq_length)

#print('DEBUG#y_train:',y_train)

y_train =  np.array([np_utils.to_categorical(seq, no_cat+1) for seq in y_train]) # Change for n-gram categorization. | 'no_cat+1' because we have PoS = 0 for "no word"
y_test =  np.array([np_utils.to_categorical(seq, no_cat+1) for seq in y_test])
y_val =  np.array([np_utils.to_categorical(seq, no_cat+1) for seq in y_val])

### end of DATASET SECTION ###

### MODEL SECTION ###
'''
input_layer = Input(shape = (seq_length,), dtype='int32')

emb = Embedding(input_dim = num_words, output_dim = num_features, input_length = seq_length, mask_zero = False)(input_layer)

forwards = LSTM(128, return_sequences=True)(emb)
backwards = LSTM(128, return_sequences=True, go_backwards=True)(emb)
common = merge([forwards, backwards], mode='concat', concat_axis=-1)
hidden = TimeDistributed(Dense(128, activation='tanh'))(common)
out = TimeDistributed(Dense(no_cat+1, activation='softmax'))(hidden)
#crf = ChainCRF(out)


### Compile model graph

model = Model(input=input_layer, output=out)



'''
### MODEL Sequential


'''
CRF MODEL


model = Sequential()
model.add(Embedding(input_dim = num_words, input_shape = (seq_length,),output_dim = num_features, input_length = seq_length, mask_zero = False))
#model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(128, return_sequences=True)))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(no_cat+1)))
model.add(Dropout(0.2))
crf = ChainCRF()
model.add(crf)
model.compile(optimizer='adam', loss=crf.loss, metrics=['accuracy','precision','recall','fmeasure'])
'''


model = Sequential()
model.add(Embedding(input_dim = num_words, input_shape = (seq_length,),output_dim = num_features, input_length = seq_length, mask_zero = False))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(128, return_sequences=True)))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(128, activation='tanh')))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(no_cat+1, activation='softmax')))



#model.compile(optimizer='adam', loss=crf.loss, metrics=['accuracy','precision','recall','fmeasure'])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy','precision','recall','fmeasure'])



### end of MODEL SECTION ###

### TRAINING SECTION ###t
model.fit(x_train, y_train, batch_size = 512
          , nb_epoch = 10, validation_data = (x_val, y_val))
### end of TRAINING SECTION ###

### PREDICTION SECTION ###
score = model.evaluate(x_test, y_test)
print(score)

#print(sentence)


model.save('test2.h5')
#del model


#print model.predict([x_train[0][0]])
### end of PREDICTION SECTION ###
