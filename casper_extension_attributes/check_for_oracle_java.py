#!/usr/bin/env python

'''
Casper extension attribute for determining
if Oracle's Java 7 runtime is installed on
OS X clients.
'''

import os

ORACLE_JAVA_DIR = '/Library/Application Support/Oracle/Java'

def main():
    if os.path.isdir(ORACLE_JAVA_DIR):
        print '<result>Installed</result>'
    else:
        print '<result>Not Installed</result>'

if __name__ == '__main__':
    main()
