# RookiePM

- Yet another [Nix](https://nixos.org) inspired package manager

## Installation

- Depends python3 and the requests library

```
git clone --depth 1 https://github.com/18fadly-anthony/rookie
cd rookie
./rookie.py --init
./rookie.py -c rookie local $(pwd)/rookie.py
./rookie.py -i rookie
```

- Then add ~/.rookie/bin to PATH

## Usage

```
rookie --add-repo example https://18fadly-anthony.github.io/rookie-repo-example/
rookie --update-repos
rookie -i neofetch           # install a package
rookie -r neofetch           # remove a package
```
