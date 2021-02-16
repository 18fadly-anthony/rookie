#!/usr/bin/env python3

import os
import argparse
import re
import requests
import hashlib
import shutil
from distutils.dir_util import copy_tree

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

def download_file(url, dest_path):
    r = requests.get(url)

    with open(dest_path, 'wb') as f:
        f.write(r.content)


def hash_file(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


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


def make_new_generation():
    gendir = rookiedir + "/generations/"
    if os.path.isdir(file_read(rookiedir + "/current_generation")):
        copy_tree(file_read(rookiedir + "/current_generation"), gendir + str(len(os.listdir(gendir)) + 1))
    else:
        mkdirexists(gendir + str(len(os.listdir(gendir)) + 1))


def switch_to_generation(new_gen):
    file_overwrite(home + "/.rookie/current_generation", new_gen)
    if os.path.isdir(rookiedir + "/bin"):
        os.remove(rookiedir + "/bin")
    os.symlink(new_gen, rookiedir + "/bin")


def install_package(package):
    # Validate package defined
    if os.path.isdir(home + "/.rookie/definitions/" + package[0]):
        if os.path.isdir(home + "/.rookie/store/" + package[0]):

            package_name = package[0]
            package_store_dir = rookiedir + "/store/" + package_name

            gendir = rookiedir + "/generations/"

            make_new_generation()

            new_gen = gendir + str(len(os.listdir(gendir)))

            if os.path.isfile(new_gen + "/" + package_name):
                os.remove(new_gen + "/" + package_name)
            os.symlink(package_store_dir + "/latest", new_gen + "/" + package_name)

            switch_to_generation(new_gen)

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
    download_file(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + package_name)

    package_store_dir = rookiedir + "/store/" + package_name

    mkdirexists(package_store_dir)
    package_hash = hash_file(rookiedir + "/tmp/" + package_name)
    mkdirexists(package_store_dir + "/" + package_hash)
    mkdirexists(package_store_dir + "/" + package_hash + "/bin")

    if not os.path.isfile(package_store_dir + "/" + package_hash + "/bin/" + package_name):
        shutil.move(rookiedir + "/tmp/" + package_name, package_store_dir + "/" + package_hash + "/bin/" + package_name)
        os.chmod(package_store_dir + "/" + package_hash + "/bin/" + package_name, 0o777)
    if os.path.isfile(package_store_dir + "/latest"):
        os.remove(package_store_dir + "/latest")
    os.symlink(package_store_dir + "/" + package_hash + "/bin/" + package_name, package_store_dir + "/latest")

    install_package(package) # Call install again after the package has been updated


def list_packages():
    package_list = os.listdir(rookiedir + "/bin")
    print("There are " + str(len(package_list)) + " package(s) installed:")
    print()
    for i in package_list:
        print(i)


def list_definitions():
    def_list = os.listdir(rookiedir + "/definitions")
    print("There are " + str(len(def_list)) + " package(s) defined:")
    print()
    for i in def_list:
        print(i)


def list_generations():
    gen_list = os.listdir(rookiedir + "/generations")
    print("There are " + str(len(gen_list)) + " generation(s):")
    print()
    print(gen_list)


def remove(package):
    package_name = package[0]
    package_list = os.listdir(rookiedir + "/bin")
    gendir = rookiedir + "/generations/"
    if package_name in package_list:
        make_new_generation()
        new_gen = gendir + str(len(os.listdir(gendir)))
        os.remove(new_gen + "/" + package_name)
    switch_to_generation(new_gen)


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: Yet Another Nix/Guix Inspired Package Manager''',
        epilog="""Copyright (C) TODO placeholder put something here""")

    parser.add_argument('--init', action='store_true', help='Setup RookiePM')
    parser.add_argument('--create', metavar=('<package>', '<type>', '<url>'), nargs=3, type=str, default="", help='Define <package> of <type> [script, tarball, appimage], with <url>')
    parser.add_argument('--install', metavar='<package>', nargs=1, type=str, default="", help='Install <package>')
    parser.add_argument('--update', metavar='<package>', nargs=1, type=str, default="", help='Update <package>')
    parser.add_argument('--upgrade', action='store_true', help='update all packages')
    parser.add_argument('--remove', metavar='<package>', nargs=1, type=str, default="", help='Remove <package>')
    parser.add_argument('--list-packages', action='store_true', help='List packages')
    parser.add_argument('--list-definitions', action='store_true', help='List package definitions')
    parser.add_argument('--list-generations', action='store_true', help='List generations')
    parser.add_argument('--switch', metavar='<generation>', nargs=1, type=int, default=0, help='Switch to <generation>')

    args = parser.parse_args()

    # print(args) # For testing

    # After arguments defined
    if args.init:
        init()

    elif args.create != '':
        create(args.create)

    elif args.install != '':
        install_package(args.install)

    elif args.update != '':
        update_package(args.update)

    elif args.list_packages:
        list_packages()

    elif args.list_definitions:
        list_definitions()

    elif args.list_generations:
        list_generations()

    elif args.switch != 0:
        switch_to_generation(rookiedir + "/generations/" + str(args.switch[0]))

    elif args.remove != '':
        remove(args.remove)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
