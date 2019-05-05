# Word guessing game.
# The game is over if user successfully guessed the word.
# User can exit the game, reload the word and give up.

import sys
from random import choice


# Path to file which contains words
FILE_PATH = 'C:\\Users\\Valentyn\\Desktop\\dict.txt'

def word_guessing_game():

    # File opening and choosing random line(=word for current file) from txt
    try:
        with open(FILE_PATH, 'r') as f:
            word = choice(f.readlines())

            # Creating list from string and removing newline (last) symbol from the word
            word_list = list(word[:-1])

    # Errors catching while file opening
    except:
        print('Could not open file by location: ', FILE_PATH)
        sys.exit(-1)

    # Creating alphabet list to check user's input
    alphabet = []

    # Creating alphabet list to check if user have already chosen this letter
    remaining_alphabet = []

    # Alphabets letters filling using the ASCII table, only English uppercase letters are using
    for letter in range(65, 91):
        alphabet.append(chr(letter))
        remaining_alphabet.append(chr(letter))

    # Word guessed progress
    word_guessed = list('_' * len(word_list))

    # Initialization a variable of user's attempts.
    attempts_cnt = 1

    print('Welcome to word guessing game! Please use only uppercase letter\n'
          'Enter 'RESTART' if you want to choose new word\n'
          'Enter 'EXIT' if you want to end the game\n'
          'Enter 'GIVE UP' if you want to stop the game and learn the guessed word\n')

    print(''.join(word_guessed))

    # Game process
    while word_list != word_guessed:

        # User's input
        user_input = input('Your choice:')

        # Option to exit the game
        if user_input == 'EXIT':
            print('Bye!')
            sys.exit(1)

        # Option to reload the word. All progress is resetting
        if user_input == 'RESTART':
            word_guessing_game()

        # Option to stop the game and learn the guessed word
        if user_input == 'GIVE UP':
            print('Better luck next time! You didn't guess the word:', word)
            sys.exit(2)

        # Check if user's input is valid
        if user_input in alphabet:

            # Check if user have already chosen this letter
            if user_input in remaining_alphabet:

                # Removing the used letter
                remaining_alphabet.remove(user_input)

                # Check if the word contains user's letter
                if user_input in word_list:

                    # Finding the position of guessed letters
                    matches = [i for i, x in enumerate(word_list) if x == user_input]

                    # 'Opening' guessed letters
                    for i in matches:
                        word_guessed[i] = user_input

                    # Printing the current word guessing progress
                    print(''.join(word_guessed))

                else:
                    attempts_cnt += 1
                    print(''.join(word_guessed))
                    print('No luck, the letter', user_input, 'is not in this word. Please try again')
            else:
                print('You have already entered this letter. Please try another')
        else:
                print('Incorrect input. Please use only upper-case symbols')
    else:
        print('Congratulations! The guessed word:', word, '\nCount of your attempts:', attempts_cnt)
        sys.exit(0)

# Function calling
word_guessing_game()

