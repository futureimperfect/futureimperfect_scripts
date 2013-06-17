#!/bin/sh

# ---------------------------------------------------------------------+
# This script adds a root certificate to the System Keychain on OS X.  |
#                                                                      |
# Created by James Barclay (james@everythingisgray.com) on 2013-06-06  |
# ---------------------------------------------------------------------+

security="/usr/bin/security"
system_keychain="/Library/Keychains/System.keychain"

# Change these
certificate="/Library/Application Support/Certificates/foo.cer"
log="/var/logs/foo.log"

# Redirection
exec >> $log 2>&1

if [ $EUID -ne 0 ]; then
    echo "This script must run as root. Exiting now."
    exit 1
fi

if [ -f "$certificate" ]; then
    # Add certificate to System Keychain
    $security add-trusted-cert -d -r trustAsRoot -k $system_keychain "$certificate"
else
    echo "Could not find $certificate".
    exit 1
fi

echo "`basename $0` success `date`"

exit 0
