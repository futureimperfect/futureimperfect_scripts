#!/bin/sh

#####################################################################
#  Casper Extension Attribute for determining Guest Sharing Status  #
#####################################################################

guestAFPEnabled=`/usr/bin/defaults read /Library/Preferences/com.apple.AppleFileServer guestAccess`
guestSMBEnabled=`/usr/bin/defaults read /Library/Preferences/SystemConfiguration/com.apple.smb.server AllowGuestAccess`

if [ "$guestAFPEnabled" == "0" ] && [ "$guestSMBEnabled" == "0" ]; then
    echo "<result>Guest Sharing Disabled</result>"

elif [ "$guestAFPEnabled" == "0" ] && [ "$guestSMBEnabled" == "1" ]; then
    echo "<result>Guest SMB Sharing Enabled</result>"

elif [ "$guestAFPEnabled" == "1" ] && [ "$guestSMBEnabled" == "0" ]; then
    echo "<result>Guest AFP Sharing Enabled</result>"

elif [ "$guestAFPEnabled" == "1" ] && [ "$guestSMBEnabled" == "1" ]; then
    echo "<result>Guest Sharing Enabled</result>"
fi

exit 0
