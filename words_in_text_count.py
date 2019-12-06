'''
The script based on assumption that 'a','o' or other one-symbols
and abbreviations ('ll','se','d') are the words
'''
from collections import Counter
from re import split
from sys import exit
from os import path

# Local path to your [Book.txt] file
MAIN_DIR = path.join('C:\\', 'Users', 'Valentyn_Troian', 'Desktop')


def read_file(main_dir):
    '''This function reads the file'''
    file_path = path.join(main_dir, 'book.txt')

    try:
        with open(file_path, 'r') as file_reading:
            file = file_reading.read()

    except FileNotFoundError:
        print(f'Could not find file by location: {file_path}')
        exit(-1)

    return file


def word_count(file):
    '''This function counts words in text'''
    # Splitting the file by words and applying the lowercase
    words = split(r'\W+', file.lower())
    counts = Counter()

    # Words count calculation
    for word in words:
        counts[word] += 1
    return counts

def print_sorted_keys_to_console(counts):
    '''Printing the result to the console sorted by keys alphabetically'''
    for elem in sorted(counts.items()):
        print(f'{elem[0]} : {elem[1]}')

    return 0


def main():
    '''This function starts the main control flow'''
    file = read_file(MAIN_DIR)
    counts = word_count(file)
    print_sorted_keys_to_console(counts)

if __name__ == '__main__':
    main()
