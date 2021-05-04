from __future__ import absolute_import

import argparse
import datetime
import json
import os
from itertools import groupby
from operator import itemgetter

import requests
from six.moves import range
from twilio.rest import Client

# Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

parser = argparse.ArgumentParser()
parser.add_argument('--pincode', required=True, type=int)
parser.add_argument('--age', type=int, default=18)
parser.add_argument('--vaccine', type=str, default='COVISHIELD')
parser.add_argument('--phone', type=str)
args = parser.parse_args()

date = datetime.datetime.now().strftime("%d-%m-%Y")
session_list = []

uri = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://www.cowin.gov.in',
    'DNT': '1',
    'Referer': 'https://www.cowin.gov.in/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

client = Client(account_sid, auth_token)

for pin in range(args.pincode - 1, args.pincode + 2):
    res = requests.get(uri.format(pin=pin, date=date), headers=headers)
    for center in res.json()['centers']:
        for session in center['sessions']:
            if session['vaccine'] == args.vaccine and session['available_capacity'] > 0 and \
                args.age >= session['min_age_limit']:
                session_list.append({
                    'vaccine': session['vaccine'],
                    'date': session['date'],
                    'pincode': center['pincode'],
                    'location': center['name']
                })

msg = ''
session_list.sort(key=itemgetter('location'))

msg += '%s available for age %s at:\n' % (args.vaccine, args.age)
for location, session in groupby(session_list, key=itemgetter('location')):
    msg += '%s on: %s\n' % (location, ', '.join(s['date'].split('-')[0] for s in session))

if session_list and args.phone:
    client.messages.create(messaging_service_sid=messaging_service_sid, body=msg, to=args.phone)

