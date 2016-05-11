# This state installs some commonly needed packages and settings

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


# Make sure Norwegian locale is available
norwegian-locale:
  locale.present:
    - name: nb_NO.UTF-8
