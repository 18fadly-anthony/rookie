#!/usr/bin/env python3

# Copyright (c) 2022 Anthony Fadly (18fadly.anthony@gmail.com)
# This program is licensed under GNU LGPL
# You are free to copy, modify, and redistribute the code.
# See COPYING file.

# Tool to convert old repo style to json

import os
import json
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


def tree_files(path):
    file_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list


def tree_dirs(path):
    dir_list = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            dir_list.append(os.path.join(root, name))
    return dir_list


def file_read(filename):
    f = open(filename, "r")
    return f.read()


def file_overwrite(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()


def convert_repo(directory, output):
    result = []
    for i in tree_dirs(directory):
        package_name = os.path.basename(i)
        package = {package_name:[]}
        for j in tree_files(i):
            package[package_name].append({os.path.basename(j): file_read(j)})
        result.append(package)
    return json.dumps(result)


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

    directory = args.directory[0]
    out = args.output_file[0]

    if not os.path.exists(directory):
        print("Error: directory not found " + directory)
        exit()

    if not os.path.exists(reverse_basename(out)):
        print("Error: directory not found " + reverse_basename(out))
        exit()

    file_overwrite(out, convert_repo(directory, out))
    print("Wrote new repository to " + out)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexit")
        exit()
