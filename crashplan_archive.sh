#!/bin/sh

# ---------------------------------------------------------------------+
# This script will copy the latest CrashPlan database dump to          |
# the directory specified in the cp_dumps_backup_dir variable.         |
#                                                                      |
# Add the script to /etc/periodic/weekly.                              |
#                                                                      |
# Created by James Barclay (james@everythingisgray.com) on 2013-02-26  |
# ---------------------------------------------------------------------+

log="/var/log/cp_archive.log"
 
# Redirection
exec >> $log 2>&1

cp="/bin/cp"
cp_dumps_dir=/Library/"Application Support"/CrashPlan/PROServer/dumps/
cp_dumps_backup_dir="~/Dropbox/crashplan_db_dumps/"
current_cp_dump=`/bin/ls /Library/Application\ Support/CrashPlan/PROServer/dumps/ | /usr/bin/grep "$(date '+%Y-%m-%d')"`

if [ ${#current_cp_dump} == "0" ]; then
    echo "Unable to find the current CrashPlan DB dump in $cp_dumps_dir."
    exit 1
fi

if [ -d "$cp_dumps_dir" ]; then
    if [ -d "$cp_dumps_backup_dir" ]; then
        $cp /Library/Application\ Support/CrashPlan/PROServer/dumps/$current_cp_dump "$cp_dumps_backup_dir" && echo "Copied $current_cp_dump to $cp_dumps_backup_dir."
    else
        echo "Unable to copy the CrashPlan DB dump. $cp_dumps_backup_dir does not exist."
        exit 1
    fi
else
    echo "Unable to copy the CrashPlan DB dump. $cp_dumps_dir does not exist."
    exit 1
fi

exit 0
