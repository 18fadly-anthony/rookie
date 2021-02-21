# RookiePM: Yet another [Nix](nixos.org) inspired package manager

## Installation

Install python3 and requests, in many GNU/Linux distros, requests is in the python standard library but on NixOS it is not

```
$ git clone --depth 1 https://github.com/18fadly-anthony/rookie
```

Put add rookie.py to your PATH, alternatively you can install rookie with itself like this:

```
$ ./rookie.py --init

$ ./rookie.py --create rookie.py local $(pwd)/rookie.py

$ ./rookie.py --install rookie.py
```

Then add ~/.rookie/bin to PATH

## Usage

```
$ rookie.py --add-repo example https://18fadly-anthony.github.io/rookie-repo-example/

$ rookie.py --update-repos

$ rookie.py --list-definitions # look at the pacakges in the repo

$ rookie.py --install neofetch # install a package

$ rookie.py --remove neofetch # remove a package

$ rookie.py --list-generations # look at the generations

$ rookie.py --switch <generation> # switch generations
```

Appimage support requires appimage-run
