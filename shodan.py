#!/usr/bin/env python

import shodan
import sys

API_KEY="5ISgqbZ9usGsN9MP1yv5LiYTzrj4HhKm"
try:
	api=shodan.Shodan(API_KEY)

	query = ' '.join('port:2375 X-Content-Type-Options: nosniff country:"CN"')
	result=api.search(query)
	for service in result['matches']:
		print service['ip_str']
except Exception as e:
	print 'error :%s'%e
	
