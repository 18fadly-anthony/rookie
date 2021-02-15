with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "rookie-env";
  buildInputs = [
    # System requirements.
    readline

    # Python requirements
    python3Packages.requests
  ];
  src = null;
  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)

    # Augment the dynamic linker path
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${R}/lib/R/lib:${readline}/lib
  '';
}
