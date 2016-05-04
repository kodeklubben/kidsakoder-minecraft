# This state installs some commonly needed packages

# Install python packages
python-pkgs:
  pkg.installed:
    - names:
      - python
      - python-pip
      - python-dev
      - python-virtualenv

# Install odbc dependencies required for pyodbc
odbc-dependencies:
  pkg.installed:
    - names:
      - unixodbc-dev
