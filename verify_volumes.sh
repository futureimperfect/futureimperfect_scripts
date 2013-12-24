#!/bin/bash

diskutil="/usr/sbin/diskutil"

echo "Verifying all mounted volumes..."

for volume in $(/bin/df | /usr/bin/awk '/\/dev\// { print $1 }' | /usr/bin/sort)
    do
        echo "Volume: $volume"
        $diskutil verifyVolume "$volume"
        echo ""
    done

exit $?
