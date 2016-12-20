import numpy

filenames = ['training', 'test','validation']

x = range(0,13)
y = ['','A','C','D','I','J','N','P','V','R','T','X','Z']
map = dict(zip(y, x))

dir = '/home/ktagowski/Downloads/gdl/data/korpus/'

def parse_file(filename):

    f = open(filename+".txt",'r')
    out_sentences = open(dir + filename + '/sentences.txt','w')
    out_tags = open(dir + filename + '/pos.txt','w')
    print dir + filename + '/sentences.txt'
    print dir + filename + '/pos.txt'
    sentence_length = range(0,104)
    counters = numpy.zeros(104)

    sentence_dict = dict(zip(sentence_length,counters))
    sentence_size = 10
    sentence = []
    tags = []
    count = 0
    for line in f:
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
            if len(sentence) != 1 and len(sentence) > sentence_size:
                out_sentences.write(" ".join(sentence) + "\n")
                out_tags.write(' '.join(str(x) for x in tags) + "\n")
                sentence_dict[len(sentence)] = sentence_dict[len(sentence)] + 1
                count = count+1
            sentence = []
            tags = []
        else:
            sentence.append(word)
            tags.append(tag)

        if len(sentence) > sentence_size:
            out_sentences.write(" ".join(sentence) + "\n")
            out_tags.write(' '.join(str(x) for x in tags) + "\n")
            sentence_dict[len(sentence)] = sentence_dict[len(sentence)] + 1
            count = count + 1
            sentence = []
            tags = []

    f.close()
    out_sentences.close()
    out_tags.close()
    print 'Sentences = ' + str(count)


for file in filenames:
    parse_file(file)

#print " ".join(sentence)
#print ' '.join(str(x) for x in tags)