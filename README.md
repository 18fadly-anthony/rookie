# RookiePM: Yet another [Nix](https://nixos.org) inspired package manager

## Installation

Install python3 and requests, in many GNU/Linux distros, requests is in the python standard library but on NixOS it is not

```
$ git clone --depth 1 https://github.com/18fadly-anthony/rookie
```

Put add rookie.py to your PATH, alternatively you can install rookie with itself like this:

```
$ ./rookie.py --init
$ ./rookie.py -c rookie local $(pwd)/rookie.py
$ ./rookie.py -i rookie
```

Then add ~/.rookie/bin to PATH

## Usage

```
$ rookie --add-repo example https://18fadly-anthony.github.io/rookie-repo-example/
$ rookie --update-repos
$ rookie -i neofetch           # install a package
$ rookie -r neofetch           # remove a package
```
