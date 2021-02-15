#!/usr/bin/env python3

import os
import argparse
import re
import urllib.request

home = os.path.expanduser('~')
rookiedir = home + "/.rookie"


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


def file_append(filename, contents):
    f = open(filename, "a")
    f.write(contents)
    f.close()


def file_overwrite(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()


def file_read(filename):
    f = open(filename, "r")
    return f.read()


# Define Package Manager Functions
def init():
    mkdirexists(home + "/.rookie")
    mkdirexists(home + "/.rookie/definitions")
    mkdirexists(home + "/.rookie/generations")
    mkdirexists(home + "/.rookie/store")
    mkdirexists(home + "/.rookie/tmp")
    file_overwrite(home + "/.rookie/current_generation", "0")


def create(q):
    valid_package_types = ["script"] # TODO add appimage,tarball, git
    if os.path.isdir(home + "/.rookie/definitions"):
        if q[1] in valid_package_types:
            if validate_url(q[2]):
                mkdirexists(home + "/.rookie/definitions/" + q[0])
                file_overwrite(home + "/.rookie/definitions/" + q[0] + "/name", q[0])
                file_overwrite(home + "/.rookie/definitions/" + q[0] + "/type", q[1])
                file_overwrite(home + "/.rookie/definitions/" + q[0] + "/url", q[2])
            else:
                print("Error: url is not valid")
        else:
            print("Error, that is not a valid package type, the valid package types are: " + str(valid_package_types))
    else:
        print("Error: please run --init first")


def install_package(package):
    # Validate package defined
    if os.path.isdir(home + "/.rookie/definitions/" + package[0]):
        if os.path.isdir(home + "/.rookie/store/" + package[0]):
            pass
        else:
            update_package(package)
    else:
        print("Error: " + package[0] + " is not defined, try: --create")


def update_package(package):
    package_name = package[0]
    if file_read(rookiedir + "/definitions/" + package_name + "/type") == "script":
        update_script(package)


def update_script(package):
    package_name = package[0]
    urllib.request.urlretrieve(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + "/" + package_name)
    #install_package(package) # Call install again after the package has been updated


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

    elif args.install != '':
        install_package(args.install)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
