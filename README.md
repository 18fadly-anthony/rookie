# RookiePM: Yet another [Nix](nixos.org) inspired package manager

## Installation

```
# Install python3

$ pip install requests # or install with nix

$ git clone --depth 1 https://github.com/18fadly-anthony/rookie

# put rookie.py in PATH

$ rookie.py --init

# add ~/.rookie/bin to PATH

```

# Usage

```
$ rookie.py --add-repo example https://18fadly-anthony.github.io/rookie-repo-example/

$ rookie.py --update-repos

$ rookie.py --list-definitions # look at the pacakges in the repo

$ rookie.py --install neofetch # install a package

$ rookie.py --remove neofetch # remove a package

$ rookie.py --list-generations # look at the generations

$ rookie.py --switch <generation> # switch generations
```
