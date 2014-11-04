meetupNotify
============

Using the meetup.com API to be notified when an event is posted.

REQUIREMENTS:
Access to a gmail account

Download main.py and save an args.yaml file in the same folder.

Include the variables below, heeding to the notes, in the args.yaml file and run your script:

$ python main.py

The variables:

seconds: must be a positive integer! Interval of time between checks and how far back it checks for when the event was updated

key: meetup.com API key

groupURLName: URL Name of meetup.com group

username: gmail account username used to send the notification email

password: gmail account password used to send the notification email

rotations: must be a positive integer! Number of times the script checks in with meetup.com

fromaddr: email address the notification email is sent from

toaddrs: email address the notification email is sent to