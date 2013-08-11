#!/bin/sh

###################################################################
#  Casper Extension Attribute for determining Guest Login Status  #
###################################################################

echo "<result>`/usr/bin/defaults read /Library/Preferences/com.apple.loginwindow | awk '/GuestEnabled/ { print $3 }' | sed 's/;//g'`</result>"

exit 0
