import imaplib
from imaplib_connect import open_connection

with imaplib_connect.open_connection() as c:
    typ, data = c.select('INBOX')
    typ, msg_ids = c.search(None, '(UNSEEN)',)
    print('Message IDs:', msg_ids)
