#!/usr/bin/env python

# JSS API script to get policy ids
# Created by James Barclay on 2013-11-26

import base64
import urllib2
import xml.etree.ElementTree as ET

# Replace with your JSS URL and a
# read-only API username and password
apiuser = 'username'
apipass = 'password'
jss_url = 'https://jss.foo.com:8443/'

url = jss_url + 'JSSResource/policies'
req = urllib2.Request(url)
base64String = base64.encodestring('%s:%s' % (apiuser, apipass)).replace('\n', '')
req.add_header('Authorization', 'Basic %s' % base64String)
resp = urllib2.urlopen(req)
data = resp.read()

root = ET.fromstring(data)
items = root.findall('./policy/id')

policy_ids = []

for item in items:
    policy_ids.append(int(item.text))

policy_ids.sort()

print policy_ids
