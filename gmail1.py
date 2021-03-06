import imaplib, getpass, email, os, re
from datetime import datetime, date, time

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
artist = []
venue = []
date_of_show = []
city = []
concert = []

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
			occurs = event_data.split('\r\n')[3]
			raw_date = datetime.strptime(occurs[:-4], "%A, %B %d, %Y %I:%M %p")
			artist = event_data.split('\r\n')[0]
			venue = event_data.split('\r\n')[1]
			city = event_data.split('\r\n')[2]
			if raw_date.date() > date.today():
				#artist = event_data.split('\r\n')[0]
				#venue = event_data.split('\r\n')[1]
				#city = event_data.split('\r\n')[2]
				#date_of_show.append(raw_date)
				#artist.append(event_data.split('\r\n')[0])
				#venue.append(event_data.split('\r\n')[1])
				#city.append(event_data.split('\r\n')[2])
				date_of_show = raw_date.strftime("%A, %B %d %Y at %I:%M %p")
				concert.append("<b>" + artist + "</b><br />" + venue + "<br />" + city + "<br />" + date_of_show + "<br />")

for show in concert:
	print show