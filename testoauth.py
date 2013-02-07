import oauth2 as oauth
import oauth2.clients.imap as imaplib

# Set up your Consumer and Token as per usual. Just like any other
# three-legged OAuth request.
consumer = oauth.Consumer('955724022201.apps.googleusercontent.com', 'uSo45SZzjwRurVOCYekgUSYW')
client = oauth.Client(consumer)
print consumer
print client

scope = 'https://mail.google.com/'
uri = 'urn:ietf:wg:oauth:2.0:oob'

authentication = 'https://accounts.google.com/o/oauth2/auth'
client_key = '955724022201.apps.googleusercontent.com'

token = oauth.Token('your_users_3_legged_token', 
    'your_users_3_legged_token_secret')

# Setup the URL according to Google's XOAUTH implementation. Be sure
# to replace the email here with the appropriate email address that
# you wish to access.
url = "https://mail.google.com/mail/b/your_users_email@gmail.com/imap/"

conn = imaplib.IMAP4_SSL('imap.googlemail.com')
conn.debug = 4 

# This is the only thing in the API for impaplib.IMAP4_SSL that has 
# changed. You now authenticate with the URL, consumer, and token.
conn.authenticate(url, consumer, token)

# Once authenticated everything from the impalib.IMAP4_SSL class will 
# work as per usual without any modification to your code.
conn.select('INBOX')
print conn.list()