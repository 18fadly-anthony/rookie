#!/usr/bin/env python3

# Copyright (c) 2021 Anthony Fadly (18fadly.anthony@gmail.com)
# This program is licensed under GNU LGPL
# You are free to copy, modify, and redistribute the code.
# See COPYING file.

import os
import argparse
import re
import requests
import hashlib
import shutil
import sys
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

    file_overwrite(dest_path, r.content.decode("utf-8").strip('\n'))


def hash_file(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_file_to_array(filename):
    content_array = []
    with open(filename) as f:
        for line in f:
            content_array.append(line.rstrip('\n'))
        return(content_array)


# Define Package Manager Functions
def init():
    mkdirexists(home + "/.rookie")
    mkdirexists(home + "/.rookie/definitions")
    mkdirexists(home + "/.rookie/generations")
    mkdirexists(home + "/.rookie/store")
    mkdirexists(home + "/.rookie/tmp")
    mkdirexists(home + "/.rookie/repos")
    file_overwrite(home + "/.rookie/current_generation", home + "/.rookie/generations/0")
    file_overwrite(home + "/.rookie/latest_generation", "0")


def create(q):
    valid_package_types = ["script", "appimage", "local"]
    need_url_types = ["script", "appimage"]
    need_local_types = ["local"]
    if os.path.isdir(home + "/.rookie/definitions"):
        if q[1] in valid_package_types:
            if q[1] in need_url_types:
                if validate_url(q[2]):
                    mkdirexists(home + "/.rookie/definitions/" + q[0])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/name", q[0])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/type", q[1])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/url", q[2])
                else:
                    print("Error: url is not valid")
            elif q[1] in need_local_types:
                if os.path.isfile(q[2]):
                    mkdirexists(home + "/.rookie/definitions/" + q[0])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/name", q[0])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/type", q[1])
                    file_overwrite(home + "/.rookie/definitions/" + q[0] + "/url", q[2])
                else:
                    print("Error: file does not exist")
        else:
            print("Error, that is not a valid package type, the valid package types are: " + str(valid_package_types))
    else:
        print("Error: please run --init first")


def add_repo(args):
    if validate_url(args[1]):
        file_overwrite(rookiedir + "/repos/" + args[0], args[1])
    else:
        print("Error: url is not valid")


def make_new_generation():
    gendir = rookiedir + "/generations/"

    new_gen = gendir + str(int(file_read(rookiedir + "/latest_generation")) + 1)
    mkdirexists(new_gen)
    old_gen = file_read(rookiedir + "/current_generation")
    if os.path.isdir(old_gen):
        package_list = os.listdir(old_gen)
        for i in package_list:
            os.symlink(os.readlink(rookiedir + "/store/" + i + "/latest"), new_gen + "/" + i)


def switch_to_generation(new_gen):
    package_list = os.listdir(new_gen)
    for i in package_list:
        package_store_dir = rookiedir + "/store/" + i
        file_overwrite(file_read(package_store_dir + "/latest_hash") + "/reference", new_gen)
    file_overwrite(rookiedir + "/current_generation", new_gen)
    gen_number = int(os.path.basename(file_read(rookiedir + "/current_generation")))
    old_gen_number = int(file_read(rookiedir + "/latest_generation"))
    if gen_number > old_gen_number:
       file_overwrite(rookiedir + "/latest_generation", str(gen_number))
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
            new_gen = gendir + str(int(file_read(rookiedir + "/latest_generation")) + 1)
            make_new_generation()
            if os.path.isfile(new_gen + "/" + package_name):
                os.remove(new_gen + "/" + package_name)
            os.symlink(os.readlink(package_store_dir + "/latest"), new_gen + "/" + package_name)
            switch_to_generation(new_gen)
        else:
            update_package(package)
    else:
        print("Error: " + package[0] + " is not defined, try: --create")


def update_package(package):
    package_name = package[0]
    defdir = rookiedir + "/definitions/"
    package_type = file_read(defdir + package_name + "/type")
    if package_type == "script":
        update_script(package)
    elif package_type == "appimage":
        update_appimage(package)
    elif package_type == "local":
        update_local(package)
    elif package_type == "versioned_script":
        update_versioned_script(package)
    else:
        print("Error: unknown package type")


def create_appimage_wrapper(wrapper_path, appimage_path):
    file_overwrite(wrapper_path, '#!/bin/sh')
    file_append(wrapper_path, '\n')
    file_append(wrapper_path, 'appimage-run ' + appimage_path)


def update_appimage(package):
    package_name = package[0]
    print("Downloading package: " + package_name + "...")
    download_file(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + package_name)
    package_store_dir = rookiedir + "/store/" + package_name
    mkdirexists(package_store_dir)
    package_hash = hash_file(rookiedir + "/tmp/" + package_name)
    mkdirexists(package_store_dir + "/" + package_hash)
    mkdirexists(package_store_dir + "/" + package_hash + "/bin")

    if not os.path.isfile(package_store_dir + "/" + package_hash + "/" + package_name):
        shutil.move(rookiedir + "/tmp/" + package_name, package_store_dir + "/" + package_hash + "/" + package_name + ".appimage")
        wrapper_path = package_store_dir + "/" + package_hash + "/bin/" + package_name
        appimage_path = package_store_dir + "/" + package_hash + "/" + package_name + ".appimage"

        create_appimage_wrapper(wrapper_path, appimage_path)

        os.chmod(wrapper_path, 0o777)
    else:
        os.remove(rookiedir + "/tmp/" + package_name)

    if os.path.isfile(package_store_dir + "/latest"):
        os.remove(package_store_dir + "/latest")
    os.symlink(package_store_dir + "/" + package_hash + "/bin/" + package_name, package_store_dir + "/latest")
    file_overwrite(package_store_dir + "/latest_hash", package_store_dir + "/" + package_hash)
    install_package(package) # Call install again after the package has been updated


def update_script(package):
    package_name = package[0]
    print("Downloading package: " + package_name + "...")
    download_file(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + package_name)

    package_store_dir = rookiedir + "/store/" + package_name

    mkdirexists(package_store_dir)
    package_hash = hash_file(rookiedir + "/tmp/" + package_name)
    mkdirexists(package_store_dir + "/" + package_hash)
    mkdirexists(package_store_dir + "/" + package_hash + "/bin")

    if not os.path.isfile(package_store_dir + "/" + package_hash + "/bin/" + package_name):
        shutil.move(rookiedir + "/tmp/" + package_name, package_store_dir + "/" + package_hash + "/bin/" + package_name)
        os.chmod(package_store_dir + "/" + package_hash + "/bin/" + package_name, 0o777)
    else:
        os.remove(rookiedir + "/tmp/" + package_name)
    if os.path.isfile(package_store_dir + "/latest"):
        os.remove(package_store_dir + "/latest")
    file_overwrite(package_store_dir + "/latest_hash", package_store_dir + "/" + package_hash)
    os.symlink(package_store_dir + "/" + package_hash + "/bin/" + package_name, package_store_dir + "/latest")

    install_package(package) # Call install again after the package has been updated


def update_versioned_script(package):
    package_name = package[0]
    package_store_dir = rookiedir + "/store/" + package_name
    repo_version = int(file_read(rookiedir + "/definitions/" + package_name + "/version"))
    if os.path.isdir(package_store_dir):
        if os.path.isfile(package_store_dir + "/latest_hash"):
            package_hash = file_read(package_store_dir + "/latest_hash")
            if os.path.isdir(package_hash):
                if os.path.isfile(package_hash + "/version"):
                    cur_version = int(file_read(package_hash + "/version"))
                    if not repo_version > cur_version:
                        print("Already up to date")
                        return

    print("Downloading package: " + package_name + "...")
    download_file(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + package_name)
    package_hash = hash_file(rookiedir + "/tmp/" + package_name)
    mkdirexists(package_store_dir)
    mkdirexists(package_store_dir + "/" + package_hash)
    mkdirexists(package_store_dir + "/" + package_hash + "/bin")
    if not os.path.isfile(package_store_dir + "/" + package_hash + "/bin/" + package_name):
        shutil.move(rookiedir + "/tmp/" + package_name, package_store_dir + "/" + package_hash + "/bin/" + package_name)
        os.chmod(package_store_dir + "/" + package_hash + "/bin/" + package_name, 0o777)
    else:
        os.remove(rookiedir + "/tmp/" + package_name)
        # But versioning should prevent this wasteful scenario from ever happening so if it does than something went wrong...
    if os.path.isfile(package_store_dir + "/latest"):
        os.remove(package_store_dir + "/latest")
    file_overwrite(package_store_dir + "/" + package_hash + "/version", str(repo_version))
    file_overwrite(package_store_dir + "/latest_hash", package_store_dir + "/" + package_hash)
    os.symlink(package_store_dir + "/" + package_hash + "/bin/" + package_name, package_store_dir + "/latest")

    install_package(package) # Call install again after the package has been updated


def update_local(package):
    package_name = package[0]
    defdir = rookiedir + "/definitions/"
    shutil.copyfile(file_read(rookiedir + "/definitions/" + package_name + "/url"), rookiedir + "/tmp/" + package_name)
    package_store_dir = rookiedir + "/store/" + package_name
    mkdirexists(package_store_dir)
    package_hash = hash_file(rookiedir + "/tmp/" + package_name)
    mkdirexists(package_store_dir + "/" + package_hash)
    mkdirexists(package_store_dir + "/" + package_hash + "/bin")
    if not os.path.isfile(package_store_dir + "/" + package_hash + "/bin/" + package_name):
        shutil.move(rookiedir + "/tmp/" + package_name, package_store_dir + "/" + package_hash + "/bin/" + package_name)
        os.chmod(package_store_dir + "/" + package_hash + "/bin/" + package_name, 0o777)
    else:
        os.remove(rookiedir + "/tmp/" + package_name)
    if os.path.isfile(package_store_dir + "/latest"):
        os.remove(package_store_dir + "/latest")
    file_overwrite(package_store_dir + "/latest_hash", package_store_dir + "/" + package_hash)
    os.symlink(package_store_dir + "/" + package_hash + "/bin/" + package_name, package_store_dir + "/latest")
    install_package(package) # Call install again after the package has been updated


def list_packages():
    package_list = os.listdir(rookiedir + "/bin")
    print("There are " + str(len(package_list)) + " package(s) installed:")
    print()
    for i in package_list:
        print(i + " (" + file_read(rookiedir + "/definitions/" + i + "/type") + ")")


def list_definitions():
    def_list = os.listdir(rookiedir + "/definitions")
    print("There are " + str(len(def_list)) + " package(s) defined:")
    print()
    for i in def_list:
        print(i + " (" + file_read(rookiedir + "/definitions/" + i + "/type") + ")")


def list_generations():
    gen_list = os.listdir(rookiedir + "/generations")
    gen_list.sort(key=int)
    current_gen = file_read(rookiedir + "/current_generation")
    print("There are " + str(len(gen_list)) + " generation(s):")
    print()
    for i in gen_list:
        packages_in_gen = os.listdir(rookiedir + "/generations/" + i)
        sys.stdout.write(i + ": ")
        for j in packages_in_gen:
            sys.stdout.write(j + " ")
        if rookiedir + "/generations/" + i == current_gen:
            sys.stdout.write("(current)")
        print()


def remove(package):
    package_name = package[0]
    package_list = os.listdir(rookiedir + "/bin")
    gendir = rookiedir + "/generations/"
    new_gen = gendir + str(int(os.path.basename(file_read(rookiedir + "/current_generation"))) + 1)
    if package_name in package_list:
        make_new_generation()
        os.remove(new_gen + "/" + package_name)
    switch_to_generation(new_gen)


def upgrade():
    package_list = os.listdir(rookiedir + "/bin")
    for i in package_list:
        update_package([i])


def find_hashes_to_gc():
    for i in os.listdir(rookiedir + "/store"):
        package_store_dir = rookiedir + "/store/" + i
        for j in os.listdir(package_store_dir):
            if os.path.isdir(package_store_dir + "/" + j):
                reference = file_read(package_store_dir + "/" + j + "/reference")
                if not os.path.isdir(reference):
                    shutil.rmtree(package_store_dir + "/" + j)
    for i in os.listdir(rookiedir + "/store"):
        package_store_dir = rookiedir + "/store/" + i
        if not os.path.isdir(file_read(package_store_dir + "/latest_hash")):
            shutil.rmtree(package_store_dir)


def garbage_collect():
    for i in os.listdir(rookiedir + "/generations"):
        path = rookiedir + "/generations/" + i
        if path != file_read(rookiedir + "/current_generation"):
            shutil.rmtree(path)
    find_hashes_to_gc()


def delete_definition(package):
    defdir = rookiedir + "/definitions/"
    storedir = rookiedir + "/store/"
    if os.path.isdir(defdir + package):
        if os.path.isdir(storedir + package):
            print("Error: package needs to be removed from store before its definition is deleted")
            print("try --remove followed by --garbage-collect")
        else:
            shutil.rmtree(defdir + package)


def update_repos():
    repodir = rookiedir + "/repos"
    defdir = rookiedir + "/definitions/"
    for i in os.listdir(repodir):
        repo = file_read(repodir + "/" + i)
        tmprepo = rookiedir + "/tmp/" + i
        download_file(repo + "/pkgs", tmprepo)
        repo_pkgs = read_file_to_array(tmprepo)
        for j in repo_pkgs:
            mkdirexists(defdir + j)
            download_file(repo + "/" + j + "/name", defdir + j + "/name")
            download_file(repo + "/" + j + "/type", defdir + j + "/type")
            download_file(repo + "/" + j + "/url", defdir + j + "/url")
            download_file(repo + "/" + j + "/version", defdir + j + "/version")
        os.remove(tmprepo)


def main():

    # Define Arguments
    parser = argparse.ArgumentParser(
        description='''RookiePM: Yet Another Nix/Guix Inspired Package Manager''',
        epilog="""Copyright (C) 2021 Anthony Fadly""")

    parser.add_argument('--init', action='store_true', help='Setup RookiePM')
    parser.add_argument('--create', metavar=('<package>', '<type>', '<url>'), nargs=3, type=str, default="", help='Define <package> of <type>, with <url>')
    parser.add_argument('--install', metavar='<package>', nargs=1, type=str, default="", help='Install <package>')
    parser.add_argument('--update', metavar='<package>', nargs=1, type=str, default="", help='Update <package>')
    parser.add_argument('--upgrade', action='store_true', help='update all packages')
    parser.add_argument('--remove', metavar='<package>', nargs=1, type=str, default="", help='Remove <package>')
    parser.add_argument('--list-packages', action='store_true', help='List packages')
    parser.add_argument('--list-definitions', action='store_true', help='List package definitions')
    parser.add_argument('--list-generations', action='store_true', help='List generations')
    parser.add_argument('--switch', metavar='<generation>', nargs=1, type=int, default=0, help='Switch to <generation>')
    parser.add_argument('--garbage-collect', action='store_true', help='Delete old generations and files')
    parser.add_argument('--delete-definition', metavar='<package>', nargs=1, type=str, default="", help='Remove <package> definition')
    parser.add_argument('--add-repo', metavar=('<name>', '<url>'), nargs=2, type=str, default='', help='Add repository')
    parser.add_argument('--update-repos', action='store_true', help='Update repositories')

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

    elif args.upgrade:
        upgrade()

    elif args.garbage_collect:
        garbage_collect()

    elif args.delete_definition != '':
        delete_definition(args.delete_definition[0])

    elif args.add_repo != '':
        add_repo(args.add_repo)

    elif args.update_repos:
        update_repos()

    else:
        print("try --help")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + "exit")
        sys.exit(0)
