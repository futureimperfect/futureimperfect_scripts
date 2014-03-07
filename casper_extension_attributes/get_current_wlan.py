#!/usr/bin/env python

'''
This script will get the current WLAN.
To be implemented as a Casper Extension
Attribute.

Created by James Barclay on 2014-02-20.

'''

import re
import subprocess

AIRPORT = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
NETWORK_SETUP = '/usr/sbin/networksetup'

def get_wireless_interface():
    '''Returns the wireless interface device
    name, (e.g., en0 or en1).'''
    hardware_ports = subprocess.check_output([NETWORK_SETUP,
                                              '-listallhardwareports'])

    match = re.search("(AirPort|Wi-Fi).*?(en\\d)", hardware_ports, re.S)
    
    wireless_interface = None
    if match:
        wireless_interface = match.group(2)

    return wireless_interface

def get_current_wlan(interface):
    '''Returns the currently connected WLAN name.'''
    wireless_status = subprocess.check_output([AIRPORT,
                                               '-I',
                                               interface]).split('\n')

    current_wlan_name = None
    for line in wireless_status:
        match = re.search(r' +SSID:\s(.*)', line)
        if match:
            current_wlan_name = match.group(1)

    return current_wlan_name

def print_current_wlan():
    '''Prints the currently connected WLAN in a
    <result></result> tag.'''
    
    wireless_interface = get_wireless_interface()
    current_wlan = get_current_wlan(wireless_interface)
    
    if current_wlan:
        print '<result>%s</result>' % current_wlan

if __name__ == '__main__':
    print_current_wlan()
