#!/usr/bin/env python

'''

             Name:  ensure_wlan_is_preferred.py
      Description:  This script ensures that PREFERRED_SSID
                    is at the top of the preferred networks
                    list.
           Author:  James Barclay <james@everythingisgray.com>
          Created:  2014-04-30
    Last Modified:  2014-06-26
          Version:  1.0

'''

from __future__ import print_function

import re
import subprocess
import time

# Constants
NETWORKSETUP = '/usr/sbin/networksetup'
PREFERRED_SSID = 'My SSID'
PREFERRED_SSID_SECURITY_TYPE = 'WPA2E'  # `man networksetup` for more info


def get_wireless_interface():
    '''Returns the wireless interface device
    name, (e.g., en0 or en1).'''
    hardware_ports = subprocess.check_output([NETWORKSETUP,
                                             '-listallhardwareports'],
                                             stderr=subprocess.STDOUT)

    match = re.search("(AirPort|Wi-Fi).*?(en\\d)", hardware_ports, re.S)

    wireless_interface = None
    if match:
        wireless_interface = match.group(2)

    return wireless_interface


def list_preferred_wireless_networks(interface):
    '''Returns a list of the preferred wireless networks.'''
    preferred_wireless_networks = subprocess.check_output([NETWORKSETUP,
                                                          '-listpreferredwirelessnetworks',
                                                          interface],
                                                          stderr=subprocess.STDOUT).split('\n')

    formatted_list = [s.strip() for s in preferred_wireless_networks]

    return formatted_list


def add_preferred_wireless_network_at_index(interface, network, index, security_type):
    '''Adds the preferred wireless network at the specified index. Does not currently
    support passing an optional password, but since we're using 802.1X I don't care.'''
    try:
        rc = subprocess.check_call([NETWORKSETUP,
                                   '-addpreferredwirelessnetworkatindex',
                                   interface,
                                   network,
                                   index,
                                   security_type],
                                   stderr=subprocess.STDOUT)

        if rc == 0:
            print('Successfully added wireless network %s to the preferred networks list.' % network)

    except subprocess.CalledProcessError as e:
        print('An error was encountered when attempting to add %s to the preferred'
              ' networks list at index %d. Error: %s', (network, index, e))


def remove_preferred_wireless_network(interface, network):
    '''Removes the specified wireless network from the preferred networks list.'''
    try:
        rc = subprocess.call([NETWORKSETUP,
                             '-removepreferredwirelessnetwork',
                             interface,
                             network],
                             stderr=subprocess.STDOUT)

        if rc == 0:
            print('Successfully removed wireless network %s from the preferred networks list.' % network)

    except subprocess.CalledProcessError as e:
        print('An error was encountered when attempting to remove %s from the'
              ' preferred networks list. Error: %s', (network, e))


def main():
    # Get the wireless interface, (e.g., en0 or en1)
    wireless_interface = get_wireless_interface()

    # Get a list of the preferred wireless networks
    preferred_wireless_networks = list_preferred_wireless_networks(wireless_interface)

    if PREFERRED_SSID in preferred_wireless_networks:
        # Remove PREFERRED_SSID from preferred networks so we can add it back at index 0
        remove_preferred_wireless_network(wireless_interface, PREFERRED_SSID)
        # Sleep for one second
        time.sleep(1)
        # Add PREFERRED_SSID to the preferred networks at position 0
        add_preferred_wireless_network_at_index(wireless_interface,
                                                PREFERRED_SSID,
                                                '0',
                                                PREFERRED_SSID_SECURITY_TYPE)
    else:
        print('%s is not in the preferred networks list.' % PREFERRED_SSID)


if __name__ == '__main__':
    main()
