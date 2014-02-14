#!/usr/bin/env python

'''
This script will get the default UTI
(Uniform Type Identifier) for the
mailto: URL scheme. To be implemented
as a Casper Extension Attribute.

Created by James Barclay on 2014-02-14.

'''

import os
import subprocess

def which(prog):
    '''Returns the path to an executable'''
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(prog)
    if fpath:
        if is_exe(prog):
            return prog
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, prog)
            if is_exe(exe_file):
                return exe_file

    return None

def is_duti_installed():
    '''Returns True if `duti` is installed'''
    if which('duti') is not None:
        return True

def get_mailto_uti():
    '''Prints the default UTI for the mailto: scheme'''
    try:
        duti = which('duti')
        uti = subprocess.check_output([duti,
                                       '-d',
                                       'mailto'])

        print '<result>%s</result>' % uti

    except subprocess.CalledProcessError, e:
        print '<result>Error: %s</result>' % e

def main():
    if is_duti_installed() is True:
        get_mailto_uti()
    else:
        print '<result>duti is not installed</result>'

main()
