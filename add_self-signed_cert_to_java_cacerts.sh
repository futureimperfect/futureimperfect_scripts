#!/bin/sh

# ------------------------------------------------------------------------+
# This script adds a self-signed certificate to the Java cacerts keystore.|
#                                                                         |
# Created by James Barclay (james@everythingisgray.com) on 2013-12-23     |
# ------------------------------------------------------------------------+

keytool="/usr/bin/keytool"
cert_path="/Library/Application Support/.CompanyName/Certificates/JavaDeploymentRuleSet"
cacerts_path="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/lib/security/cacerts"
storepass="changeit"
log="/Library/Logs/cacerts_import.log"

# Redirection
exec >> $log 2>&1

if [ $EUID -ne 0 ]; then
    echo "This script must run as root. Exiting now."
    exit 1
fi

if [ -f "$cert_path/Cert.csr" ]; then
    # Add self-signed certificate to
    # the Oracle Java cacerts keystore
    if [ -f "$cacerts_path" ]; then
        $keytool \
            -import \
            -noprompt \
            -storepass "$storepass" \
            -alias selfsigned \
            -keystore "$cacerts_path" \
            -trustcacerts \
            -file "$cert_path/Cert.csr"
    else
        echo "$cacerts_path does not exist!"
    fi
else
    echo "Could not find $cert_path/Cert.csr."
    exit 1
fi

echo "`basename $0` success `date`"

exit 0
