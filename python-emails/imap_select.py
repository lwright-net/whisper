import imaplib
import imaplib_connect

with imaplib_connect.open_connection() as c:
    typ, data = c.select('INBOX')
    print(typ, data)
    num_msg = int(data[0])
    print('There are {} messages in INBOX'.format(num_msg))
