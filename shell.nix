# shell.nix for rookie
with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "rookie-env";
  buildInputs = [
    python3
    python3Packages.requests
  ];
}
