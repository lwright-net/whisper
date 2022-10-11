import imaplib
import configparser

def open_connection(verbose=False):
    #Read the config
    config = configparser.ConfigParser()
    config.read('./py_read_mail.conf')

    #Connect to server
    hostname = config.get('server', 'hostname')
    if verbose:
        print('Connecting to', hostname)
    connection = imaplib.IMAP4_SSL(hostname)

    #Login to email account
    username = config.get('account', 'username')
    password = config.get('account', 'password')
    if verbose:
        print('Logging in as', username)
    try:
        connection.login(username,password)
        return connection
    except Exception as err:
        print('ERROR:', err)


if __name__ == '__main__':
    with open_connection(verbose=True) as c:
        print(c)
