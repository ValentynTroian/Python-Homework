# Preconditions:
# pip install xlrd
# pip install pandas

'''This program converts Excel sheets to csv files'''

from pandas import read_excel
from xlrd import XLRDError

CONFIG_PATH = r'C:\Users\Valentyn_Troian\PycharmProjects\lessons\config.txt'


def parse_config(config_path):
    '''This function parses config file and run a converting to csv to each file sheet'''

    with open(config_path, 'r') as file:
        files = file.read().splitlines()

        for line in files:
            file = line.split(',')[0]
            sheets = line.split(',')[1:]

            for sheet in sheets:
                convert_to_csv(file, sheet)


def convert_to_csv(file, sheet):
    '''This function converts xlsx sheet to separate csv file'''

    try:
        dataframe = read_excel(file, sheet_name=sheet)
        csv_name = file.replace('.xlsx', f'-{sheet}.csv')
        dataframe.to_csv(csv_name, index=False)  # 'index=False' prevents pandas to write row index

    except FileNotFoundError:
        print(f'{file} is not founded')

    except XLRDError:
        print(f'Can\'t find the sheet {sheet} of {file}')


def main():
    '''This function run a main program flow'''
    parse_config(CONFIG_PATH)


if __name__ == '__main__':
    main()
