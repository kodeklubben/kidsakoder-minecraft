# Install python packages
python-pkgs:
  pkg.installed:
    - names:
      - python
      - python-pip
      - python-dev
      - python-virtualenv
      - ipython

# Install odbc dependencies required for pyodbc
odbc-dependencies:
  pkg.installed:
    - names:
      - unixodbc-dev
