#!/usr/bin/python3

import requests
import json

## print json function
def outputPrint(data):
	for k, v in data.items():
		if isinstance (v, dict):
			print('{0}'.format(k))
			outputPrint(v)
		else:
			print('\t{0} : {1}'.format(k,v))

callsign = 'run'

## run loop
while (callsign != '0'):
	# query for callsign
	callsign = input("Callsign : ")
	print('\n')

	# move on to exit if callsign == '0'
	if (callsign != '0'):
		# build request url for api to callook.info
		apiGet =  'https://callook.info/' + callsign + '/json'

		# GET to callook.info for callsign info
		r = requests.get(apiGet)

		output = r.json()

		# print result
		outputPrint(output)
		print('\n')
	else:
		# exit message
		print('exit')

exit
