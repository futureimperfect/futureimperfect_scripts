#!/bin/sh

# ---------------------------------------------------------------------+
# This script will continuously ping a host. The packet size is        |
# 1480 bytes, (1472 + 8 for ICMP headers). The don't fragment bit      |
# is set. The script runs 15 pings every hour, and it sends alerts     |
# to the email address defined in the $email_addr variable if the      |
# maximum round trip time reaches 200 ms.                              |
#                                                                      |
# Created by James Barclay (james@everythingisgray.com) on 2012-12-13  |
# ---------------------------------------------------------------------+

ping="/sbin/ping"
tail="/usr/bin/tail"
awk="/usr/bin/awk"
printf="/usr/bin/printf"
sendmail="/usr/sbin/sendmail"

if [ $EUID -ne 0 ]; then
    echo "This script must run as root. Exiting now."
    exit 1
fi

log="/var/log/$(date '+%Y-%m-%d')_pingtest.log"
host="google.com"
name="Johnny Appleseed"
email_addr="johnny@appleseed.com"

# Redirection
exec 2>&1

echo "Starting ping test. The log file will be saved to $log."
echo "Press ^C to exit." 

for ((i=1; ; i++))
    do
    echo "Starting ping test $i on $(date)." >> $log
    $ping -c 15 -s 1472 -D -q $host >> $log
    echo " " >> $log
    max_ping=`$tail -n 2 $log | $awk '/round-trip/ { split($0, line, "/"); printf("%.0f\n", line[6]); }'`
    max_ping_float=`$tail -n 2 $log | $awk '/round-trip/ { split($0, line, "/"); printf("%s\n", line[6]); }'`
    if [ "$max_ping" -ge "200" ]; then
        echo "Max ping time reached $max_ping_float ms. Sending alert to $email_addr." >> $log
        $printf "Subject: Alert from $(HOSTNAME) - Ping Test Results\n\nHello, $name. The ping test script encountered a maximum round-trip time of $max_ping_float ms." | $sendmail -f $email_addr $email_addr
    fi
    sleep 3600
done

exit 0
