#!/usr/bin/env python3

import sys
import argparse


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: The Rookie Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    parser.add_argument('--create', metavar='', nargs=3, type=str, default="", help='<package> <type> <url>')
    parser.add_argument('--install', metavar='', nargs=1, type=str, default="", help='<package>')

    args = parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
