[(
  self: super:
  let
    myPythonPackages = {
      crontab = super.callPackage ./crontab.nix { pythonPackages = super.python3Packages; };
    };
    packageOverrides = python-self: python-super: myPythonPackages;
  in {
    python3 = super.python3.override {inherit packageOverrides;};
  }
)]
