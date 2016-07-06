import pprint
import sys
import os

import spotipy
import spotipy.util as util
import json
import urllib2
from pprint import pprint
import requests

fbToken = os.getenv('FB_TOKEN')
fbID = os.getenv('FB_ID')

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


url = 'https://api.gotinder.com/auth'
headers ={'Content-Type': 'application/json', 'User-Agent':'Tinder/4.8.2 (iPhone; iOS 9.1; Scale/2.00)'}
payload = {'force_refresh' : 'False', 'facebook_id' : fbID, 'facebook_token' : fbToken}
r = requests.post(url, headers=headers, data = json.dumps(payload))


print 'token is: ' + str(fbToken)
print 'fbid is: ' + str(fbID)

rjson =  json.loads(r.text)
print "token is: " + rjson['token']
tinder_token = rjson['token']

tinder_headers = {'X-Auth-Token': tinder_token,
                  'Authorization': 'Token token="{0}"'.format(tinder_token).encode('ascii', 'ignore')
                  }
print tinder_headers

#getting reccomandations
url2 = 'https://api.gotinder.com/user/recs'

tinder_headers2 = {'X-Auth-Token': tinder_token,
                  'Authorization': 'Token token="{0}"'.format(tinder_token).encode('ascii', 'ignore'),
                   'locale': 'en-GB'
                  }
r = requests.post(url2, headers = tinder_headers2)
with open('data.txt', 'w') as outfile:
    json.dump(r.text, outfile, sort_keys=True, indent=4)
with open('data.txt') as data_file:
    recs_json = json.load(data_file)
#pprint(recs_json)
recs_json2 = byteify(recs_json)
print r.url
print r.headers
print r.request
print r.status_code

dict = json.loads(recs_json2)

print type(dict)
for i in dict['results']:
    print i['_id']
#print type(recs_json2)
#pprint(recs_json2)



like_headers2 = {'X-Auth-Token': tinder_token,
                   'Authorization': 'Token token="{0}"'.format(tinder_token).encode('ascii', 'ignore'),
                   'firstPhotoID': 'en-GB'
                   }


