{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    pkgs.python311Packages.pydantic
    pkgs.python311Packages.fastapi
    pkgs.python311Packages.uvicorn
  ];

  env = {
    PYTHONPATH = ".";
  };
}