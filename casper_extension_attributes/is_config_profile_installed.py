#!/usr/bin/env python

'''
This script determines if the specified
configuration profile is installed. To
be implemented as a Casper Extension
Attribute.

Created by James Barclay on 2014-02-13.

'''

import subprocess

PROFILE_UUID = '00000000-0000-0000-0000-000000000000'

def is_config_profile_installed():
    installed_profiles = subprocess.check_output(['/usr/bin/profiles',
                                                  '-C'])
    if PROFILE_UUID in installed_profiles:
        print '<result>Installed</result>'
    else:
        print '<result>Not installed</result>'

is_config_profile_installed()
