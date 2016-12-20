import sys

f = open(sys.argv[1], 'r')
o = open('sentences.txt', 'w')
for line in f:
    if line == '\n':
        continue
    o.write(line)
f.close()
o.close()

f = open(sys.argv[2], 'r')
o = open('pos.txt', 'w')
for line in f:
    if line == '\n':
        continue
    o.write(line)
f.close()
o.close()
