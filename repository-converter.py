#!/usr/bin/env python3

# Copyright (c) 2022 Anthony Fadly (18fadly.anthony@gmail.com)
# This program is licensed under GNU LGPL
# You are free to copy, modify, and redistribute the code.
# See COPYING file.

# Tool to convert old repo style to json

import os
import argparse

home = os.path.expanduser('~')


def main():
    parser = argparse.ArgumentParser(
        description = '''Repo converter for RookiePM''',
        epilog = """Copyright (C) 2021 Anthony Fadly""")

    parser.add_argument('-d', '--directory', metavar = '<directory>', nargs = 1,
                        type = str, default = home + "/.rookie/definitions",
                        help = "directory with old definitions")

    parser.add_argument('-o', '--output-file', metavar = '<output file>', nargs = 1,
                        type = str, default = home + "/.rookie/definitions/definitions.json",
                        help = "output file")

    args = parser.parse_args()

    print(args.directory)
    print(args.output_file)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexit")
        exit()
