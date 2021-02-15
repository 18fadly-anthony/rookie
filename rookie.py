#!/usr/bin/env python3

import sys
import argparse


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: The Rookie Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    parser.add_argument('--create', metavar='', nargs=3, type=str, default="", help='<package> <type> <url> - Define <package> of <type> [script, tarball, appimage], with <url>')
    parser.add_argument('--sync', metavar='', nargs=1, type=str, default="", help='<package> - Sync (install and upgrade) <package>')
    parser.add_argument('--sync-all', metavar='', help='Sync all installed packages')

    args = parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
