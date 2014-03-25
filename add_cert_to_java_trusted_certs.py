#!/usr/bin/env python

'''
This script allows you to import a certificate into
the Oracle Java trusted.certs keystore. It assumes
that the certificate you want to add to the keystore
exits in /private/tmp.

Created by James Barclay on 2014-03-10.

'''

from __future__ import print_function

import os
import plistlib
import subprocess
import sys

# Constants
ALIAS            = 'your_alias'
INTERNET_PLUGINS = '/Library/Internet Plug-Ins'
JAVA_CERT        = '/private/tmp/your_cert.cer'

JAVA_WEB_PLUGIN  = os.path.join(INTERNET_PLUGINS, 'JavaAppletPlugin.plugin')

def get_console_user():
    '''Returns the currently logged-in user as
    a string, even if running as EUID root.'''
    if os.geteuid() == 0:
        console_user = subprocess.check_output(['/usr/bin/stat',
                                                '-f%Su',
                                                '/dev/console']).strip()
    else:
        import getpass
        console_user = getpass.getuser()

    return console_user

def determine_java_vendor(info_plist):
    '''Determine Java vendor. Takes the path to
    a Java Info.plist file and returns a string
    of the Java vendor's name.'''
    java_vendor = None
    try:
        pl = plistlib.readPlist(info_plist)
        java_vendor = pl['CFBundleIdentifier'].split('.')[1]

    except KeyError:
        print('CFBundleIdentifer does not exist in %s.' % info_plist)

    except IOError:
        print('%s does not exist!' % info_plist)

    return java_vendor

def get_keytool_path(java_vendor):
    '''Returns the path to the keytool command-
    line utility.'''
    keytool_path = None
    if java_vendor == 'oracle':
        keytool_path = os.path.join(JAVA_WEB_PLUGIN, 'Contents/Home/bin/keytool')
    elif java_vendor == 'apple':
        keytool_path = '/usr/bin/keytool'

    return keytool_path

def cert_in_keystore(keytool, keystore, store_pass, alias):
    '''Returns True if the specified certificate
    alias exists in the specified keystore.'''
    try:
        if os.path.exists(keystore):
            rc = subprocess.check_call([keytool,
                                        '-list',
                                        '-keystore',
                                        keystore,
                                        '-storepass',
                                        store_pass,
                                        '-alias',
                                        alias])
            if rc == 0:
                return True

    except subprocess.CalledProcessError, e:
        print('An error occurred when attempting to locate alias \'%s\' in %s. Probably ok. Error: %s' % (alias, keystore, e))

def add_cert_to_java_trusted_certs(keytool, store_pass, cert, keystore):
    '''Adds the specified certificate to the specified
    Java cacerts keystore.'''
    try:
        subprocess.check_output([keytool,
                                 '-import',
                                 '-v',
                                 '-noprompt',
                                 '-storepass',
                                 store_pass,
                                 '-alias',
                                 ALIAS,
                                 '-keystore',
                                 keystore,
                                 '-trustcacerts',
                                 '-file',
                                 cert])
    except subprocess.CalledProcessError, e:
        print('An error occurred when attempting to add %s to %s. Error: %s.' % (cert, keystore, e))

def main():
    real_java_path = os.path.realpath(JAVA_WEB_PLUGIN)
    java_info_plist = os.path.join(real_java_path, 'Contents/Info.plist')
    java_vendor = determine_java_vendor(java_info_plist)
    trusted_certs = '/Users/%s/Library/Application Support/Oracle/Java/Deployment/security/trusted.certs' % get_console_user()

    keytool = os.path.join(JAVA_WEB_PLUGIN, 'Contents/Home/bin/keytool')
    if not os.path.isfile(keytool):
        keytool = '/usr/bin/keytool'

    store_pass = ''
    if not os.path.isfile(trusted_certs):
        store_pass = 'changeit'

    if os.path.exists(JAVA_CERT):
        if java_vendor == 'oracle':
            if cert_in_keystore(keytool, trusted_certs, store_pass, ALIAS):
                print('%s already exists in %s. Exiting now.' % (ALIAS, trusted_certs))
                sys.exit(1)
            else:
                print('Using %s to add %s to %s.' % (keytool, JAVA_CERT, trusted_certs))
                add_cert_to_java_trusted_certs(keytool, store_pass, JAVA_CERT, trusted_certs)
        elif java_vendor == 'apple':
            print('Unable to add certificate to trusted.certs. Modify com.apple.java.security.plist instead.')
            sys.exit(1)
        else:
            print('Unable to continue. Unknown Java vendor: %s.' % java_vendor)
            sys.exit(1)
    else:
        print('%s does not exist! Exiting now.' % JAVA_CERT)
        sys.exit(1)

if __name__ == '__main__':
    main()
