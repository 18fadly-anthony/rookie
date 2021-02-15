#!/usr/bin/env python3

import sys
import argparse


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: The Rookie Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
