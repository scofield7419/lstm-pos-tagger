import numpy as np
import math

filenames = ['training', 'test','validation']
#filenames = ['training']


x = range(0,13)
y = ['','A','C','D','I','J','N','P','V','R','T','X','Z']
tags_map = dict(zip(y, x))

dir = '../../data/korpus/'

def parse_file(filename,max_sentence_length):
    # = 11
    f = open(filename+".txt",'r')
    out_sentences = open(dir + filename + '/sentences.txt','w')
    out_tags = open(dir + filename + '/pos.txt','w')
    #print dir + filename + '/sentences.txt'
  #  print dir + filename + '/pos.txt'
    sentence_length = range(0,105)
    counters = np.zeros(105)
    sentence_dict = dict(zip(sentence_length,counters))
   # sentence_size = 10

    words = []
    tags = []
    count = 0

    # Syntax : Zatrzasnął	zatrzasnąć	VqMS-------P---
    #         Word [0]      unused      Tags [2] Used_only first Tag
    for line in f:
       # print (line)
        if line=="\n":
            if len(words) !=0:
                if len(words) < max_sentence_length+1:
                    out_sentences.write(" ".join(words) + "\n")
                    out_tags.write(' '.join(str(x) for x in tags) + "\n")
                    sentence_dict[len(words)] = sentence_dict[len(words)] + 1
                    count = count + 1
                else:
                    #splitowanie po n zdan
                    '''
                    print (len(words))
                    nlen = math.ceil(len(words) / float(max_sentence_length))
                    print (nlen)
                    words = np.array(words)
                    words = np.array_split(words,nlen)
                    for arr in words:
                        print (arr.tolist())
                    '''

              #  if len(words) == 1:
                 #   print(words)
                 #   print(tags)

            words = []
            tags = []
        else:
            tagged_word = line.split("\t")

            word = tagged_word[0] #word
           # some mistakes in dataset like
            # z globalizowania	zglobalizowanie	NNNS2----------
            # removing white spaces
            word = ''.join(word.split())
            pos_tag = tagged_word[2][0] #only first tag needed
            pos_tag = tags_map[pos_tag]

            #print(word + " " + str(pos_tag))
           # if len(tagged_word) > 3:
            #    print (line)

            words.append(word)
            tags.append(pos_tag)



        '''
        #print line
        string = line.split("\t")
        word = string[0]
        if string.__len__() > 1:
            tag = string[2][0]
            tag = map[tag]
        else:
            tag = ""
       # print word + " " + str(tag);
        #print string
        if line=="\n":
            if len(sentence) != 1 and len(sentence) < sentence_size+1:
                print(sentence)
                out_sentences.write(" ".join(sentence) + "\n")
                out_tags.write(' '.join(str(x) for x in tags) + "\n")
                sentence_dict[len(sentence)] = sentence_dict[len(sentence)] + 1
                count = count+1
            sentence = []
            tags = []
        else:
            sentence.append(word)
            tags.append(tag)

      #  if len(sentence) > sentence_size:
       #     out_sentences.write(" ".join(sentence) + "\n")
       #     out_tags.write(' '.join(str(x) for x in tags) + "\n")
       #     sentence_dict[len(sentence)] = sentence_dict[len(sentence)] + 1
       #     count = count + 1
       #     sentence = []
        #    tags = []
    '''

    print (sentence_dict)
    for key in sentence_dict:
        print(str(key) + ';' + str(sentence_dict[key]) + ';')
    f.close()
    out_sentences.close()
    out_tags.close()
    print ('Sentences = ' + str(count))


for file in filenames:
    parse_file(file,max_sentence_length=5)

#print " ".join(sentence)
#print ' '.join(str(x) for x in tags)
