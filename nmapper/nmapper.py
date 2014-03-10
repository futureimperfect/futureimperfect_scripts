#!/usr/bin/env python

'''
This program does OS fingerprinting on the
networks passed to it in a CSV with the
`nmap` utility. The networks in the CSV
file must be in CIDR notation. Do not
include headers in the CSV file.

Created by James Barclay on 2014-03-10.

'''

import csv
import os
import subprocess
import sys

from optparse import OptionParser

def is_root():
    '''Returns true if running as the root user.'''
    if os.geteuid() == 0:
        return True

def nmap_csv_reader(path):
    '''Takes a path to a CSV file with subnets and does
    OS fingerprinting on each network..'''
    with open(path[0], 'rU') as csv_file:
        try:
            cidrs = csv.reader(csv_file,
                               delimiter=' ',
                               quotechar='|',
                               dialect=csv.excel_tab)
            for cidr in cidrs:
                nmapper(cidr[0])

        except csv.Error as e:
            sys.exit('File: %s, Error: %s' % (path[0], e))

def nmapper(cidr):
    '''Runs the nmap command with the specified options
    on the CIDR network passed to it.'''
    try:
        output = subprocess.check_output(['nmap',
                                          '-sV',
                                          '-O',
                                          '-v',
                                          cidr])
        print output

    except subprocess.CalledProcessError, e:
        print 'Error: %s' % e


def main():
    p = OptionParser()
    p = OptionParser(description='''This program does OS fingerprinting on the networks passed to it in a CSV with the `nmap` utility. The networks in the CSV file must be in CIDR notation. Do not include headers in the CSV file.
''',
                     prog='nmapper',
                     version='nmapper 0.1',
                     usage= 'python %prog.py /path/to/subnets.csv')

    (options, arguments) = p.parse_args()

    if not is_root():
        print 'This program requires root privileges. Try \'sudo %s\' instead.' % os.path.basename(__file__)
        sys.exit(1)

    if len(arguments) == 1:
        nmap_csv_reader(arguments)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
