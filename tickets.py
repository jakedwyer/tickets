#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging

import cgi, cgitb
from urllib2 import urlopen
from json import load, dumps
import imaplib, getpass, email, os, re
from datetime import datetime, date, time

#cgitb.enable()


form = cgi.FieldStorage() 

#user = raw_input('enter email: ')
#pwd = raw_input('enter password: ')

user = form.getvalue('user')
pwd = form.getvalue('pwd')

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

concert = []

for emailid in items[::-1]:
	resp, data = mail.fetch(emailid, "(RFC822)")

	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_string(response_part[1])
			subject=msg['subject']
			payload=msg.get_payload()
			body=extract_body(payload)
			event = body.split(' to:\r\n\r\n')
			event = event[1].split('Order for:')
			event_data = event[0]
			occurs = event_data.split('\r\n')[3]
			raw_date = datetime.strptime(occurs[:-4], "%A, %B %d, %Y %I:%M %p")
			artist = event_data.split('\r\n')[0]
			venue = event_data.split('\r\n')[1]
			city = event_data.split('\r\n')[2]
			if raw_date.date() > date.today():
				date_of_show = raw_date.strftime("%A, %B %d %Y at %I:%M %p")
				concert.append("<p><b>" + artist + "</b><br />" + venue + "<br />" + city + "<br />" + date_of_show + "<br />")
				
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Your Upcoming Shows</title>"
print "</head>"
print "<body>"
print "<h2>Your Upcoming Shows</h2>" 
for show in concert:
	print show
print "</body>"
print "</html>"
