#!/usr/bin/env python3

# Mostly cribbed from here: https://superuser.com/questions/394516/how-to-convert-50-episodes-from-dvd-into-50-mp4-with-handbrake-easily

import os
import re
import subprocess
import sys


def main():
    preset = 'Super HQ 1080p30 Surround'

    # Ugly but simple way to get first argument = folder with DVD
    # We will get DVD name by removing all / and \
    dvd = sys.argv[1]
    if len(sys.argv) < 3:
        dvd_name = re.sub(r'.*[/\\]', r'', dvd).rstrip('/').rstrip('\\')
    else:
        # Set `dvd_name` manually if desired.
        dvd_name = sys.argv[2]

    while True:
        try:
            season = int(input('Season: '))
            break
        except ValueError:
            print('Enter a digit.')

    disc = None
    while True:
        try:
            disc = int(input('Disc (Control-C for None): '))
            break
        except ValueError:
            print('Enter a digit.')
        except KeyboardInterrupt:
            break

    cmd = ['HandBrakeCLI', '-i', f'{dvd}', '-t', '0']
    s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    count = 0
    for line in s.stdout:
        if re.search(rb"\+ title [0-9]+:", line):
            count += 1
    print(f'==Extracting {count} chapters from "{dvd}"==')

    for i in range(1, count+1):
        if disc:
            output = f'{dvd_name}_season_{season:02}_disc_{disc:02}_episode_{i:02}.mp4'
        else:
            output = f'{dvd_name}_season_{season:02}_episode_{i:02}.mp4'
        cmd = [
            'HandBrakeCLI',
            '--input',
            f'{dvd}',
            '--title',
            f'{i}',
            '--preset',
            # 'Normal',
            f'{preset}',
            '--output',
            f'{output}'
        ]
        log = f"encoding_{output}.log"
        with open(log, 'wb') as f:
            s = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
            s.communicate()
        if not os.path.isfile(output):
            print(f'ERROR during extraction of "{output}"!')
        else:
            print(f'Successfully extracted Chapter #{i} to "{output}"')

    # Eject the disc. Why doesn't this work?
    _ = subprocess.check_output(['drutil', 'eject'])


if __name__ == '__main__':
    main()
