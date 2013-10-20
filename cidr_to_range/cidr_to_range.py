#!/usr/bin/env python

import csv
import pprint
import sys

from netaddr import *

csv_file = sys.argv[1]

def cidrToRange(csv_file):
    with open(csv_file, 'rU') as csvfile:
        cidrNetworks = csv.reader(csvfile, delimiter=' ', quotechar='|', dialect=csv.excel_tab)
        for address in cidrNetworks:
            addressStrings = '\n'.join(address)
            ip = IPNetwork(addressStrings)
            ip_list = list(ip)

            beginningAddress = ip_list[0]
            endingAddress = ip_list[-1]

            print '%s - %s' % (beginningAddress, endingAddress)

        csvfile.close()

cidrToRange(csv_file)
