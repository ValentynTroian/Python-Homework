# The script based on assumption that 'a','o' or other one-symbols and abbreviations ('ll','se','d') are the words

from re import split
from sys import exit
from os import path

# Local path to your [Book.txt] file
MAIN_DIR = path.join('C:', 'Users', 'Valentyn', 'Desktop')


def read_file():
    
    file_path = path.join(MAIN_DIR, 'Book.txt')

    try:
        with open(file_path, 'r') as f:
            file = f.read()

    except FileNotFoundError:
        print('Could not find file by location: ', file_path)
        exit(-1)

    return file


def word_count(file):

    # Splitting the file by words and applying the lowercase
    words = split('\W+', file.lower())

    counts = dict()

    # Words count calculation
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # Printing the result in usable format
    for i in counts:
        print(i, ':', counts[i])

    return counts


def main():
    file = read_file()
    word_count(file)


if __name__ == '__main__':
    main()
