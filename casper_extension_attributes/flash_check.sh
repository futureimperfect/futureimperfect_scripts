#!/bin/bash

#####################################################################
#  Casper Extension Attribute for determining Flash Player version  #
#####################################################################

_defaults="/usr/bin/defaults"
flash_path="/Library/Internet Plug-Ins/Flash Player.plugin/Contents"

if [ -d "$flash_path" ]; then
    echo "<result>`"$_defaults" read "$flash_path"/Info CFBundleShortVersionString`</result>"
else
    echo "<result>Not installed</result>"
fi

exit 0
