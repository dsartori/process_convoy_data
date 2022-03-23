import os
import json
import re

aggregate={}
canadaPostal = {}
canadaFSA = {}

source = 'data'
directory = os.fsencode(source)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith('.json'):
		filepath = os.path.join(source,filename)
		with open(filepath,'r') as f:
			data = json.load(f)
			postal = data['billing_details']['address']['postal_code'].replace(" ","").upper()
			val = data['amount']
			if postal in aggregate:
				aggregate[postal] += val
			else:
				aggregate[postal] = val

for postal in aggregate:
	if not postal.isnumeric() and len(postal) == 6 and re.search('[A-Z][0-9][A-Z][0-9][A-Z][0-9]',postal) != None:
		canadaPostal[postal]=aggregate[postal]

for postal in canadaPostal:
	fsa = postal[0:3]
	val = canadaPostal[postal]
	if fsa in canadaFSA:
		canadaFSA[fsa] += val
	else:
		canadaFSA[fsa] = val

f = open('output/postal.csv','w')
for postal in canadaPostal:
	f.write(postal + ',' + str(canadaPostal[postal]) + '\n')
f.close

f = open('output/fsa.csv','w')
for fsa in canadaFSA:
	f.write(fsa + ',' + str(canadaFSA[fsa]) + '\n')
f.close


