''' 
Word guessing game.
The game is over if user successfully guessed the word.
User can exit the game, reload the word and give up.
'''

from sys import exit
from random import choice
from os import path

# Path to file which contains words
FILE_PATH = path.join('C:', 'Users', 'Valentyn_Troian', 'Desktop', 'dict.txt')


def read_file_and_choose_random_word():
    '''This function read file and choose random word'''
    # File opening and choosing random line(=word for current file) from txt
    try:
        with open(FILE_PATH, 'r') as f:
            word = choice(f.readlines())

            # Creating list from string and removing newline (last) symbol from the word
            letter_list = list(word[:-1])

    except FileNotFoundError:
        print('Could not open file by location: ', FILE_PATH)
        exit(-1)

    return letter_list


def create_alphabets():
    '''This function creates alphabets'''
    # Creating alphabet list to check user's input
    alphabet = []

    # Creating alphabet list to check if user have already chosen this letter
    remaining_alphabet = []

    # Alphabets letters filling using the ASCII table, only English uppercase letters are using
    for letter in range(65, 91):
        alphabet.append(chr(letter))
        remaining_alphabet.append(chr(letter))

    return alphabet, remaining_alphabet


def guess_process(letter_list, alphabet, remaining_alphabet):
    '''This function ...'''
    # Word guessed progress
    word_guessed = list('_' * len(letter_list))

    # Initialization a variable of user's attempts.
    attempts_cnt = 1

    print('Welcome to word guessing game! Please use only uppercase letter\n'
          'Enter [RESTART] if you want to choose new word\n'
          'Enter [EXIT] if you want to end the game\n'
          'Enter [GIVE UP] if you want to stop the game and learn the guessed word\n')

    print(''.join(word_guessed))

    # Game process
    while letter_list != word_guessed:

        # User's input
        user_input = input('Your choice:').upper()

        # Option to exit the game
        if user_input == 'EXIT':
            print('Bye!')
            exit(1)

        # Option to reload the word. All progress is resetting
        if user_input == 'RESTART':
            guess_process(letter_list, alphabet, remaining_alphabet)

        # Option to stop the game and learn the guessed word
        if user_input == 'GIVE UP':
            print('Better luck next time! You didn\'t guess the word:', ''.join(letter_list))
            exit(2)

        # Check if user's input is valid
        if user_input in alphabet:

            # Check if user have already chosen this letter
            if user_input in remaining_alphabet:

                # Removing the used letter
                remaining_alphabet.remove(user_input)

                # Check if the word contains user's letter
                if user_input in letter_list:

                    # Finding the position of guessed letters
                    matches = [i for i, x in enumerate(letter_list) if x == user_input]

                    # 'Opening' guessed letters
                    for i in matches:
                        word_guessed[i] = user_input

                    # Printing the current word guessing progress
                    print(''.join(word_guessed))

                else:
                    attempts_cnt += 1
                    print(''.join(word_guessed))
                    print(f'No luck, the letter {user_input} is not in this word.\
                            Please try again')
            else:
                print('You have already entered this letter. Please try another')
        else:
            print('Incorrect input. Please use only english symbols')
    else:
        print('Congratulations! The guessed word:', ''.join(letter_list), '\n'
              'Count of your attempts:', attempts_cnt)

    return 0


def main():
    '''This function starts main control flow'''
    letter_list = read_file_and_choose_random_word()
    alphabet, remaining_alphabet = create_alphabets()
    guess_process(letter_list, alphabet, remaining_alphabet)


if __name__ == '__main__':
    main()
