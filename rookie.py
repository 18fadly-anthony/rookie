#!/usr/bin/env python3

import sys
import argparse


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: The Rookie Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    # parser.add_argument('--foo', type=int, default=42, help='FOO!')
    # parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')

    args=parser.parse_args()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
