#!/usr/bin/env python3

import os
import argparse

home = os.path.expanduser('~')


def mkdirexists(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)


def init():
    mkdirexists(home + "/.rookie")
    mkdirexists(home + "/.rookie/definitions")
    mkdirexists(home + "/.rookie/generations")


def create(q):
    mkdirexists(home + "/.rookie/definitions/" + q[0])


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: The Rookie Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    parser.add_argument('--init', action='store_true', help='Setup RookiePM')
    parser.add_argument('--create', metavar=('<package>', '<type>', '<url>'), nargs=3, type=str, default="", help='Define <package> of <type> [script, tarball, appimage], with <url>')
    parser.add_argument('--sync', metavar='<package>', nargs=1, type=str, default="", help='Sync (install and upgrade) <package>')
    parser.add_argument('--sync-all', metavar='', help='Sync all installed packages')
    parser.add_argument('--remove', metavar='<package>', nargs=1, type=str, default="", help='Remove <package>')
    parser.add_argument('--purge', metavar='<package>', nargs=1, type=str, default="", help='Remove <package> definition')
    parser.add_argument('--list-packages', metavar='', help='List packages')
    parser.add_argument('--list-definitions', metavar='', help='List package definitions')
    parser.add_argument('--list-generations', metavar='', help='List generations')
    parser.add_argument('--switch', metavar='<generation>', nargs=1, type=int, default=0, help='Switch to <generation>')
    parser.add_argument('--gc', metavar='', help='Garbage collect (delete) all past generation')

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
