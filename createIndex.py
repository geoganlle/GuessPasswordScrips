# how to use createIndex.py
#
# Enter the following command on the console :
#
# python createIndex.py 6 8 pw.text
#
# position  |value            |description                   |
#:--------- |:----------------|:-----------------------------|
# param1:   |createIndex.py : | the name of this scrips      |
# param2:   |6 :              | min number of password places|
# param3:   |8 :              | max number of password places|
# param4:   |pw.text :        | ouput file                   |


import sys
import string
import itertools

def get_strings():
    #chars = string.printable[:62]
    chars = string.printable[:10]
    strings = []
    for i in range(min, max + 1):
        strings.append((itertools.product(chars, repeat=i),))
    return itertools.chain(*strings)

def make_dict():
    f = open(file, 'w+')
    for x in list_str:
        for y in x:
            f.write("".join(y))
            f.write('\n')
    f.close()
    print()
    'Done'

while True:
    if len(sys.argv) == 4:
        try:
            min = int(sys.argv[1])
            max = int(sys.argv[2])
        except:
            print()
            "wrong"
            sys.exit(0)
        if min <= max:
            list_str = get_strings()
            file = sys.argv[3]
            make_dict()
            sys.exit(0)  

#  python createIndex.py 6 6 pw.text