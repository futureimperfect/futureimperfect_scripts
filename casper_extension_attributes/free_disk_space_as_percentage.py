#!/usr/bin/env python

# This script gets the percentage of disk space used
# on the startup disk in OS X. Implemented as a Casper
# Extension Attribute.

import subprocess
import re

def printDiskUsageAsPercent():
    df = subprocess.Popen(["df", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    filesystem, blocks, used, available, percent, iused, ifree, percentiused, mountpoint = \
	output.split("\n")[1].split()
    diskUsageAsPercent = re.sub('\%$', '', percent)
    print '<result>%i</result>' % (int(diskUsageAsPercent))

printDiskUsageAsPercent()

