#!/usr/bin/env python3

import os
import argparse
import re

home = os.path.expanduser('~')


# Define General Functions
def mkdirexists(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return(re.match(regex, url) is not None)


# Define Package Manager Functions
def init():
    mkdirexists(home + "/.rookie")
    mkdirexists(home + "/.rookie/definitions")
    mkdirexists(home + "/.rookie/generations")
    mkdirexists(home + "/.rookie/store")


def create(q):
    valid_package_types = ["script"] # TODO add appimage,tarball, git
    if os.path.isdir(home + "/.rookie/definitions"):
        if q[1] in valid_package_types:
            if validate_url(q[2]):
                pass
            else:
                print("Error: url is not valid")
        else:
            print("Error, that is not a valid package type, the valid package types are: " + str(valid_package_types))
    else:
        print("Error: please run --init first")


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: Yet Another Nix/Guix Inspired Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    parser.add_argument('--init', action='store_true', help='Setup RookiePM')
    parser.add_argument('--create', metavar=('<package>', '<type>', '<url>'), nargs=3, type=str, default="", help='Define <package> of <type> [script, tarball, appimage], with <url>')
    parser.add_argument('--install', metavar='<package>', nargs=1, type=str, default="", help='Install <package>')
    parser.add_argument('--update', metavar='<package>', nargs=1, type=str, default="", help='Update <package>')
    parser.add_argument('--remove', metavar='<package>', nargs=1, type=str, default="", help='Remove <package>')
    parser.add_argument('--remove-store', metavar='<package>', nargs=1, type=str, default="", help='Remove <package> and remove it from the store')
    parser.add_argument('--remove-definition', metavar='<package>', nargs=1, type=str, default="", help='Remove <package>, and remove it from the store, and remove its definition')
    parser.add_argument('--list-packages', metavar='', help='List packages')
    parser.add_argument('--list-definitions', metavar='', help='List package definitions')
    parser.add_argument('--list-generations', metavar='', help='List generations')
    parser.add_argument('--switch', metavar='<generation>', nargs=1, type=int, default=0, help='Switch to <generation>')

    args = parser.parse_args()

    # After arguments defined
    if args.init:
        init()

    elif args.create != '':
        create(args.create)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
