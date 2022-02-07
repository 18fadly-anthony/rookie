#!/usr/bin/env python3

# Copyright (c) 2022 Anthony Fadly (18fadly.anthony@gmail.com)
# This program is licensed under GNU LGPL
# You are free to copy, modify, and redistribute the code.
# See COPYING file.

# Tool to convert old repo style to json

import os
import argparse

home = os.path.expanduser('~')

def reverse_basename(path):
    if not "/" in path:
        return path
    basename = os.path.basename(path)
    l = ""
    for i in path.split('/'):
        if i != basename:
            l += i
            l += "/"
    return l


def main():
    parser = argparse.ArgumentParser(
        description = '''Repo converter for RookiePM''',
        epilog = """Copyright (C) 2021 Anthony Fadly""")

    parser.add_argument('-d', '--directory', metavar = '<directory>', nargs = 1,
                        type = str, default = [home + "/.rookie/definitions"],
                        help = "directory with old definitions")

    parser.add_argument('-o', '--output-file', metavar = '<output file>', nargs = 1,
                        type = str, default = [home + "/.rookie/definitions/definitions.json"],
                        help = "output file")

    args = parser.parse_args()

    if not os.path.exists(args.directory[0]):
        print("Error: directory not found " + args.directory[0])
        exit()

    if not os.path.exists(reverse_basename(args.output_file[0])):
        print("Error: directory not found " + reverse_basename(args.output_file[0]))
        exit()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexit")
        exit()
