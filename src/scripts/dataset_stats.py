path = ''
folder = 'test/training/'
filename = 'sentences.txt'

d = dict()

f = open(path + folder + filename, 'r')
for line in f:
    arr = line.split()
    length = len(arr)
    #print (length)
    if length in d:
        d[length] += 1
    else:
        d[length] = 1

    if length > 10:
        print (arr)

print (d)


for key in d:
    print (str(key) + ';' + str(d[key]) +';')