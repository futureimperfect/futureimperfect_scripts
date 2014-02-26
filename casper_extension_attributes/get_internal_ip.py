#!/usr/bin/env python

'''
This script gets the internal IP. Useful
if your JSS is hosted externally and the
client IP reported to the JSS is the
public IP.

Created by James Barclay on 2014-02-26.

'''

import socket

def get_ip_addr():
    '''Returns the IP address.'''
    ip_addr = socket.gethostbyname(socket.gethostname())
    
    if ip_addr == '127.0.0.1':
        ip_addr = socket.gethostbyname(socket.getfqdn())
    
    return ip_addr

def print_result(result):
    '''Prints result in <result></result> tag.'''
    print('<result>%s</result>' % result)

def main():
    print_result(get_ip_addr())

if __name__ == '__main__':
    main()
