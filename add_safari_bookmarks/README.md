# add_safari_bookmarks.py

`Usage: python add_safari_bookmarks.py [-m] [</path/to/bookmarks.csv>]`

Adds bookmarks to Safari from a CSV containing bookmark titles[0] and URIs[1].
The proper format of the CSV is (title, uri). Do not include headers in the
CSV file.

## Options
      --version      show program's version number and exit
      -h, --help     show this help message and exit
      -m, --menubar  add bookmarks to Safari's menu bar instead of bookmarks bar

## TODO

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
