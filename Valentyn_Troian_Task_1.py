# The script based on assumption that 'a','o' or other one-symbols and abbreviations ('ll','se','d') are the words

import re
import sys

# File path to the file. According to needs, it would be better to use the parameters to local PC
file_path = 'C:\\Users\\Valentyn\\Desktop\\Book.txt'

# File opening and catching the errors
try:
    f = open(file_path, 'r')
except:
    print('Could not open file by location: ', file_path)
    sys.exit()

# Main
def word_count(str):
    counts = dict()

    # Splitting the text by words and applying the lowercase to the text
    text = re. split('\W+', str.lower())

    # Words count calculation
    for word in text:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # Printing the result in usable format
    for i in counts:
        print (i,':', counts[i])


# Function calling
word_count(f.read())

