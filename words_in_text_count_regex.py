'''
The script based on assumption that 'a','o' or other one-symbols
and abbreviations ('ll','se','d') are the words
'''
from collections import Counter
from re import findall
from sys import argv, exit


def read_file(argv):
    '''This function reads the file specified as 2nd parameter of command'''
    if len(argv) == 2:
        if argv[1] == '/?':
            print('The command usage: python [script_name.py] [file.txt]')
            exit(0)
        else:
            file_path = argv[1]

    else:
        print('Wrong parameters. '
              'The command usage: python [script_name.py] [file.txt]')
        exit(-1)

    try:
        with open(file_path, 'r') as file_reading:
            file = file_reading.read()

    except FileNotFoundError:
        print(f'Could not find file by location: {file_path}')
        exit(-2)

    return file


def word_count(file):
    '''This function counts words in text'''
    words = Counter(findall(r'\w+', file.lower()))
    return words


def print_sorted_keys_to_console(counts):
    '''Printing the result to the console sorted by keys alphabetically'''
    for elem in sorted(counts.items()):
        print(f'{elem[0]} : {elem[1]}')

    return 0


def main():
    '''This function starts the main control flow'''
    file = read_file(argv)
    counts = word_count(file)
    print_sorted_keys_to_console(counts)


if __name__ == '__main__':
    main()
