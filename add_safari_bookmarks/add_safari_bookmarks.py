#!/usr/bin/env python

'''
  TODO

* Support more browsers
* Support more than just Excel CSVs
* Should work if headers in CSV exist or not
* Resolve issue that occurs if the
  Bookmarks.plist has never been modified
* If URI already exists in the plist, it means
  that you can't add duplicate bookmarks to
  different locations, (e.g., Bookmarks
  Menu and Bookmarks Bar). Fix this.
* Make the default to import one bookmark
  at a time, CSV as an option
* Allow adding folders of bookmarks
* Use plistlib instead of PlistBuddy, (will
  need to convert binary plist to XML before
  modifying)

'''

import csv
import os
import subprocess
import sys

from optparse import OptionParser
from sys import platform as _platform

PLIST_BUDDY = '/usr/libexec/PlistBuddy'

def getConsoleUser():
    """Returns the currently logged in user."""
    if os.geteuid() == 0:
        console_user = subprocess.check_output(['/usr/bin/stat', '-f%Su', '/dev/console']).strip()

    else:
        import getpass
        console_user = getpass.getuser()

    return console_user

def backupBookmarks():
    """Backup current users' Safari Bookmarks.plist file"""
    os.chdir('/Users/%s/Library/Safari' % getConsoleUser())

    try:
        subprocess.check_output(['/usr/bin/zip', 'BookmarksBackup.zip', 'Bookmarks.plist'])

    except subprocess.CalledProcessError as e:
        sys.exit('error: %s' % e)

def addSafariBookmarks(bookmarksCsv, bookmarksLocation):
    """Takes a CSV file containing bookmark titles[0] and URIs[1] and uses PlistBuddy to add them to the BookmarksBar or BookmarksMenu."""
    with open(bookmarksCsv[0], 'rU') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|', dialect=csv.excel_tab)
        bookmarksPlist = '/Users/%s/Library/Safari/Bookmarks.plist' % getConsoleUser()

        try:
            f = open(bookmarksPlist, 'r')
            searchlines = f.readlines()
            f.close()

            for row in rows:

                for line in searchlines:

                    if row[1] in line:
                        break # for...else: break out of loop if uri[1] exists in plist

                else:
                    subprocess.check_output([PLIST_BUDDY,
                        '%s' % bookmarksPlist,
                        '-c',
                        'Add :Children:%d:Children:0 dict' % bookmarksLocation])
                    subprocess.check_output([PLIST_BUDDY,
                        '%s' % bookmarksPlist,
                        '-c',
                        'Add :Children:%d:Children:0:URIDictionary dict' % bookmarksLocation])
                    subprocess.check_output([PLIST_BUDDY,
                        '%s' % bookmarksPlist,
                        '-c',
                        'Add :Children:%d:Children:0:URIDictionary:title string %s' % (bookmarksLocation, row[0])])
                    subprocess.check_output([PLIST_BUDDY,
                        '%s' % bookmarksPlist,
                        '-c',
                        'Add :Children:%d:Children:0:URLString string %s' % (bookmarksLocation, row[1])])
                    subprocess.check_output([PLIST_BUDDY,
                        '%s' % bookmarksPlist,
                        '-c',
                        'Add :Children:%d:Children:0:WebBookmarkType string WebBookmarkTypeLeaf' % bookmarksLocation])

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

def main():
    p = OptionParser()
    p = OptionParser(description="""Adds bookmarks to Safari from a CSV containing bookmark titles[0] and URIs[1]. The proper format of the CSV is (title, uri). Do not include headers in the CSV file.
""",
                     prog='add_safari_bookmarks',
                     version='add_safari_bookmarks 0.1',
                     usage= 'python %prog.py [-m] /path/to/bookmarks.csv')

    p.add_option('-m', '--menubar',
                 help='add bookmarks to Safari\'s menu bar instead of bookmarks bar',
                 dest='menubar',
                 default=False,
                 action='store_true')

    (options, arguments) = p.parse_args()

    if _platform != 'darwin' or len(arguments) != 1:
        p.print_help()

    if options.menubar:
        addSafariBookmarks(arguments, int(2)) # Add bookmarks to menu bar if --menubar option is passed

    else:
        addSafariBookmarks(arguments, int(1))

if __name__ == '__main__':
    backupBookmarks()
    main()
