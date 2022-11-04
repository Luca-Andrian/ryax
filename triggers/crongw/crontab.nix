{ lib, pkgs, pythonPackages }:

pythonPackages.buildPythonPackage rec {
    pname = "crontab";
    version = "0.22.5";
    name = "${pname}-${version}";

    src = pythonPackages.fetchPypi {
      inherit pname version;
      sha256 = "4cdd1dea8d7fda6671a53a3923708c79691d05aebee7fbfd77493643614c3916";
    };

    propagatedBuildInputs = with pythonPackages; [
    ];

    doCheck = false;

    meta = with lib; {
      homepage = https://github.com/josiahcarlson/parse-crontab;
      description = "Parse and use crontab schedules in Python";
    };
}
