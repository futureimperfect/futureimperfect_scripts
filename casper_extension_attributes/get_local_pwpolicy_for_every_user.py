#!/usr/bin/env python

'''

             Name:  get_local_pwpolicy_for_every_user.py
      Description:  This script gets the local password policy
                    for every user with a uid >= 500.
           Author:  James Barclay <james@everythingisgray.com>
          Created:  2014-07-22
    Last Modified:  2014-07-22
          Version:  1.0

'''

from __future__ import print_function

import os
import pwd
import subprocess
import sys


if os.geteuid() != 0:
    print('This script must run as root. Exiting now.')
    sys.exit(1)


def get_users_with_uid_above_five_hundred():
    '''
    Return an array of users with uid's >= 500.
    '''
    greater_than_five_hundred_users = []
    accounts_to_skip = ('ausertoskip',
                        'nobody')

    for p in pwd.getpwall():
        if p[2] >= 500 and p[0].lower() not in accounts_to_skip:
            greater_than_five_hundred_users.append(p[0])

    return greater_than_five_hundred_users


def get_password_policy(user):
    '''
    Get the local password policy for user.
    '''
    password_policy = None

    try:
        password_policy = subprocess.check_output(['/usr/bin/pwpolicy',
                                                   '-u',
                                                   '%s' % user,
                                                   '--get-effective-policy']).strip()

        if password_policy:
            return password_policy
        else:
            return None

    except subprocess.CalledProcessError as e:
        password_policy = 'Could not get the local password policy for %s. Error: %s.' % (user, e)

    return password_policy


def main():
    users = get_users_with_uid_above_five_hundred()
    password_policy_string = ''

    for user in users:
        password_policy_string += '%s=%s;' % (user, get_password_policy(user))

    print('<result>%s</result>' % password_policy_string)


if __name__ == '__main__':
    sys.exit(main())
