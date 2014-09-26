#!/usr/bin/env python

'''

             Name:  shellshock_check.py
      Description:  Casper extension attribute that tells us if we're
                    vulnerable to CVE-2014-6271 or CVE-2014-7169.
           Author:  James Barclay <james@everythingisgray.com>
          Created:  2014-09-25
    Last Modified:  2014-09-25
          Version:  1.0

'''

import os
import subprocess


def six_two_seven_one(shell_path):
    '''
    @returns True if shell_path is vulnerable to CVE-2014-6271.
    '''
    cmd = 'env x=\'() { :;}; echo vulnerable\' %s -c \'echo hello\'' % shell_path
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            executable=shell_path)

    (out, err) = proc.communicate()

    if 'vulnerable' in out:
        return True

    return False


def seven_one_six_nine(shell_path):
    '''
    @returns True if shell_path is vulnerable to CVE-2014-7169.
    '''
    cmd = 'env X=\'() { (a)=>\\\' sh -c "echo cal"; cat echo'
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            executable=shell_path)

    (out, err) = proc.communicate()

    cal_days = 'Su Mo Tu We Th Fr Sa'
    if cal_days in out:
        return True

    return False


def main():
    bad_shells = []
    shells = ['/bin/bash',
              '/usr/local/bin/bash',
              '/opt/boxen/homebrew/bash',
              '/opt/local/bin/bash',
              '/bin/sh']

    for shell in shells:
        # Create our working string
        ws = ''
        # Don't bother checking if not executable
        if os.access(shell, os.X_OK):
            # Are we vulnerable to CVE-2014-6271?
            if six_two_seven_one(shell):
                ws += '(%s:CVE-2014-6271)' % shell
            # Are we vulnerable to CVE-2014-7169?
            if seven_one_six_nine(shell):
                ws += '(%s:CVE-2014-7169)' % shell

            if ws:
                bad_shells.append(ws)

    if len(bad_shells) > 0:
        print('<result>%s</result>' % ', '.join(bad_shells))
    else:
        print('<result>Patched</result>')


if __name__ == '__main__':
    main()
