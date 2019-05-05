from os import walk, listdir, path
from sys import exit

from pyodbc import connect, InterfaceError, OperationalError, ProgrammingError
from json import load
from csv import writer

from datetime import datetime
from time import time

# libraries for 'send_email' function

from smtplib import SMTP_SSL, SMTPAuthenticationError
from ssl import create_default_context
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# libraries for 'update_csv_in_gspread' function

from gspread import authorize, exceptions
from oauth2client.service_account import ServiceAccountCredentials, client


def read_config():
    '''This function reads all parameters needed for program from [config.json] file'''

    try:
        with open('config.json') as f:
            config = load(f)
            return config

    except FileNotFoundError:
        print('Can't find [config.json] in current directory. Please ensure that the file is located there')
        exit(-1)

    except OSError:
        print('OSError during [config.json] reading. Please ensure that your disk isn't full')
        exit(-2)


def connect_to_sql_server(config):
    '''This function make a connection to SQL Server'''

    try:
        connection = connect('Driver=' + config['DRIVER'] + ';'
                             'Server=' + config['SQL_SERVER_NAME'] + ';'
                             'Database=' + config['DB_NAME'] + ';'
                             'Trusted_Connection=' + config['TRUSTED_CONNECTION'])
        return connection

    except TimeoutError:
        print('Can't connect to SQL Server for long time. Please check [config.json] parameters and try again')
        exit(-3)
    except InterfaceError:
        print('Can't connect to SQL Server. Please check 'DRIVER' attribute in [config.json] and try again')
        exit(-4)
    except OperationalError:
        print('Can't connect to SQL Server. Please check 'SQL_SERVER_NAME' attribute in [config.json] and try again')
        exit(-5)
    except ProgrammingError:
        print('Can't connect to SQL Server. Please check 'DB_NAME' attribute in [config.json] and try again')
        exit(-6)


def close_sql_server_conn(connection):
    '''This function closes a connection to SQL Server'''

    try:
        connection.close()
        return 0

    except ProgrammingError:
        print('Attempt to use a closed connection. Probably you use this function twice in main')


def find_sql_files_with_traverse(config):   # The function isn't called in main by default.
    '''This function returns all sql files from current folder and all subfolders
    using [PATH_TO_SCRIPTS_FOLDER] parameter from [config.json]'''

    files_list_tr = []

    for root, dirs, files in walk(config['PATH_TO_SCRIPTS_FOLDER']):
        for file in files:
            if file.endswith('.sql'):
                files_list_tr.append(path.join(config['PATH_TO_SCRIPTS_FOLDER'], file))
    return files_list_tr


def find_sql_files_without_traverse(config):
    '''This function returns all sql files in current folder
        using [PATH_TO_SCRIPTS_FOLDER] parameter from config.json'''

    files_list = []

    for file in listdir(config['PATH_TO_SCRIPTS_FOLDER']):
        if file.endswith('.sql'):
            files_list.append(file)
    return files_list


def exec_sql_and_save_to_csv(files_list, connection, config):
    '''This function executes queries from each sql file and saves the results to csv file'''

    # Getting current datetime for name of csv file
    cur_datetime = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

    # Creating a name format for csv file
    csv_file = config['REPORT_FILE_NAME_PREFIX'] + cur_datetime + '.csv'

    # Creating a csv file and writing a header line
    try:
        with open(csv_file, 'w', newline='') as f:
            f.write('FILE_NAME,EXECUTION_STATUS,ERROR_MESSAGE,EXECUTION_TIME,OBJECT_NAME,TEST_NAME,COUNT,RESULT\n')

    except OSError:
        print('OSError during', csv_file, 'creating. Please ensure that your disk isn't full')
        exit(-7)

    for file in files_list:

        # Opening each query of sql file
        try:
            with open(file, 'r') as f:
                query = f.read()

        # Errors handling during sql file opening
        except OSError:
            print('OSError during ', file, ' opening. Please ensure that your disk isn't full')

        try:
            start_exec_time = time()

            # Query execution
            cursor = connection.cursor()
            cursor.execute(query)
            sql_output = cursor.fetchall()

            end_exec_time = time()
            exec_time = str(end_exec_time - start_exec_time)

            # Getting results of query execution, adding sql files names, execution status and time to csv output list
            file_output = [[file] + ['Query executed successfully'] + [''] + [exec_time] + list(tup) for tup in
                           sql_output]
            print(file_output)

        # Writing error messages during query execution to csv file and ending the current loop cycle
        except Exception as e:
            with open(csv_file, 'a', newline='') as f:
                f.write(file)
                f.write(',Error during query execution,')

                # Parsing and writing an error message from SQL Server
                f.write(str(e)[str(e).index('[SQL Server]') + len('[SQL Server]'):str(e).index('.')])
                f.write('\n')
                continue

        # Writing output to csv file
        try:
            with open(csv_file, 'a', newline='') as f:
                wr = writer(f)
                for row in file_output:
                    wr.writerow(row)

        except OSError:
            print('OSError during writing to ', csv_file, '. Please ensure that your disk isn't full')

    return csv_file


def send_email(csv_file, config):
    '''This function sends an email with csv file'''

    body = 'Your report is ready. Please open the attached file for more details'

    message = MIMEMultipart()
    message['From'] = config['EMAIL_SENDER']
    message['To'] = config['EMAIL_RECEIVER']
    message['Subject'] = config['ENV'] + ' Testing in: ' + config['PATH_TO_SCRIPTS_FOLDER']
    message['Cc'] = config['EMAIL_CC']

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Open csv_file file in binary mode
    with open(csv_file, 'rb') as attachment:
        # Add file as application/octet-stream
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {csv_file}',
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    password = input('Please enter your Gmail password: ')

    context = create_default_context()

    # Send the email
    with SMTP_SSL(config['SMTP_SERVER'], config['PORT'], context=context) as server:
        try:
            server.login(config['EMAIL_SENDER'], password)
            server.sendmail(config['EMAIL_SENDER'], config['EMAIL_RECEIVER'], text)
        except SMTPAuthenticationError:
            print('Uncorrect Gmail password. Please try again')
            exit(-8)
        except IOError:
            print('Your input is invalid. Please try again')
            exit(-9)
    return text


def update_csv_in_gspread(csv_file, config):
    ''' This function opens Google Sheet document and updates data from csv file'''

    # Reading the unique credentials
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(config['CREDENTIALS_FILE_NAME'])
    except FileNotFoundError:
        print('Can't find your ', config['CREDENTIALS_FILE_NAME'])

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = credentials.create_scoped(scope)

    # Authorizing using oauth2client
    try:
        gc = authorize(credentials)
    except client.HttpAccessTokenRefreshError:
        print('Invalid grant: Not a valid email or user ID. Please check your ', config['CREDENTIALS_FILE_NAME'])
        exit(-10)

    # Opening the spreadsheet
    try:
        wks = gc.open(config['G_SPREADSHEET_NAME']).sheet1
    except exceptions.SpreadsheetNotFound:
        print('Can't find the spreadsheet. Please ensure that you created the spreadsheet '
              'with name specified in the ', config['CREDENTIALS_FILE_NAME'])
        exit(-11)

    with open(csv_file, 'r') as f:
        row = 1
        column = 1

        for li in f:
            items = li.strip().split(',')

            for item in items:
                wks.update_cell(row, column, item)
                column += 1
            row += 1
            column = 1


def main():
    ''' This main function runs all needed functions for program in the right order'''

    call_config = read_config()

    call_connection = connect_to_sql_server(call_config)

    call_files_list = find_sql_files_without_traverse(call_config)

    call_csv_file = exec_sql_and_save_to_csv(call_files_list, call_connection, call_config)

    send_email(call_csv_file, call_config)

    update_csv_in_gspread(call_csv_file, call_config)

    close_sql_server_conn(call_connection)


if __name__ == '__main_':
    main()  # Calling the main function
