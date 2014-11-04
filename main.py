# Update in a args.yaml file --sitting in the same folder as the main.py-- the key, groupURLName, rotations, username and password of gmail account with your API meetup.com key,
# the URL name of your meetup group, times the script checks on the events before it ends, and your gmail account information, respectively.

# Also, update the seconds. This is the interval by which the script is scheduled to run. The seconds also define how far back the
# script looks to see if the pulled events were updated recently.

# The seconds must be a strictly positive integer!

import requests
import json
from datetime import datetime as d
import calendar
import smtplib
import sys
import time
import sched
import yaml

stream = open('./args.yaml', 'r')
arguments = yaml.load(stream)

seconds = arguments['seconds']
key = arguments['key']
groupURLName = arguments['groupURLName']
rotations = arguments['rotations']
username = arguments['username']
password = arguments['password']

def meetupNotify():
	url = 'https://api.meetup.com/2/events?&key=' + key + '&sign=true&photo-host=public&group_urlname=' + groupURLName 
	timeNow = calendar.timegm(d.utcnow().utctimetuple())
	cutoffTime = timeNow - seconds

	response = requests.get(url)

	if response.status_code != 200:
		print "There was an error retrieving the data."
		print "This is the returned status code: " + str(response.status_code)
		return "Exit of function."

	jobject = json.loads(response.text.encode(response.encoding))
	eventsCount = jobject['meta']['count']

	if eventsCount == 0:
		print "No events!"
		return "Exit of function."

	events = []
	eventDict = {}

	for event in jobject['results']:
		try:
			timeUpdated = 0
			if event['updated'] != 0:
				timeUpdated = event['updated'] / 1000
			time = 0
			if (event['time'] + event['utc_offset']) != 0:
				time = (event['time'] + event['utc_offset']) / 1000
			eventDict = dict([('id',event['id']), ('updated',timeUpdated), ('time',time), ('event_url',event['event_url']),('nameOfEvent',event['name']), ('nameOfGroup',event['group']['name'])])
			if (cutoffTime - (timeUpdated - 1)) <= 0:
				events.append(eventDict)
		except KeyError, e:
			print 'Raised a KeyError! Missing key: %s' % str(e)
			return "Exit of function."

	if events == []:
		print "No recent events."
		return "Exit of function."

	# I need to fix it so all the msg get passed.
	if len(events) > 1:
		msg = 'Subject: You have events\n\n' 
	else:
		msg = 'Subject: You have an event\n\n'
	for event in events:
		date = (d.utcfromtimestamp(int(event['time']))).strftime('%b %d %Y')
		time = (d.utcfromtimestamp(int(event['time']))).strftime('%I:%M%p')
		string = "The " + event['nameOfGroup'] + " meetup has organized \"" + event['nameOfEvent'] + "\" to happen on " + date + " at " + (time) + ". Register at: " + event['event_url']
		msg = msg + string + '\n\n'

	fromaddr = 'frenchfriedamerican@gmail.com'
	toaddrs = 'cyndie.cottrell@gmail.com'

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()


def scheduler_meetupNotify():

	scheduler.enter(0, 1, meetupNotify, ())
	scheduler.run()
	time.sleep(seconds)

scheduler = sched.scheduler(time.time, time.sleep)

for i in range(rotations):
	print "Scheduler ran %i times." % i
	scheduler_meetupNotify()

