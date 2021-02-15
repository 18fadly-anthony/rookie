#!/usr/bin/env python3

import os
import argparse

home = os.path.expanduser('~')


# Define General Functions
def mkdirexists(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)


# Define Package Manager Functions
def init():
    mkdirexists(home + "/.rookie")
    mkdirexists(home + "/.rookie/definitions")
    mkdirexists(home + "/.rookie/generations")
    mkdirexists(home + "/.rookie/store")


def create(q):
    valid_package_types = ["script"] # TODO add appimage,tarball, git
    # mkdirexists(home + "/.rookie/definitions/" + q[0]) # TODO validate type and url before creating generation


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

    if args.create != '':
        create(args.create)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
