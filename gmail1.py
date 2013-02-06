import imaplib, getpass, email, os, re
import parsedatetime as pdt

user = raw_input('enter email: ')
pwd = raw_input('enter password: ')


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, pwd)
mail.select("[Gmail]/All Mail")

#exp = re.compile("^(?=.*?(Your))(?=.*?(Ticket Order)).*$")

def extract_body(payload):
	if isinstance(payload, str):
		return payload
	else:
		return '\n'.join([extract_body(part.get_payload()) for part in payload])


resp, items = mail.search(None, '(FROM "customer_support@ticketmaster.com" SUBJECT "Ticket Order")')
items = items[0].split()

my_msg = []
msg_cnt = 0
artist = []
venue = []
date = []
city = []

for emailid in items[::-1]:
	resp, data = mail.fetch(emailid, "(RFC822)")

	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_string(response_part[1])
			subject=msg['subject']
			payload=msg.get_payload()
			body=extract_body(payload)
			#print subject + "\n"
			event = body.split(' to:\r\n\r\n')
			#print event[0]
			event = event[1].split('Order for:')
			event_data = event[0]
			#print event_data
			artist.append(event_data.split('\r\n')[0])
			venue.append(event_data.split('\r\n')[1])
			city.append(event_data.split('\r\n')[2])
			raw_date = pdt._extract_date(event_data.split('\r\n')[3])
			date.append(raw_date)
			msg_cnt += 1
			
print date
print venue
print artist