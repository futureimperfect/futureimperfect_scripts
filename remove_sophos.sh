#!/bin/sh

# ---------------------------------------------------------------------+
# This script will remove Sophos using the included removal package.   |
# It can be used as a preinstall script or in Casper if the priority   |
# is set to "Before."                                                  |
#                                                                      |
# Created by James Barclay (james@everythingisgray.com) on 2013-08-01  |
# ---------------------------------------------------------------------+

exec 2>&1

sophos_dir="/Library/Sophos Anti-Virus"
remove_sophos_av="Remove Sophos Anti-Virus.pkg"

if [ $EUID -ne "0" ]; then
    echo "This script must run as root. Exiting now."
    exit 1
fi

if [ -d "$sophos_dir" ]; then
    if [ -d "$sophos_dir/$remove_sophos_av" ]; then
        cd "$sophos_dir"
        /usr/sbin/installer -pkg "$remove_sophos_av" -target /
    else
        echo "$remove_sophos_av does not exist. Exiting now."
        exit 1
    fi
else
    echo "$sophos_dir does not exist. Exiting now."
    exit 1
fi

exit 0
