# Install Overviewer
install-overviewer:
  pkgrepo.managed:
    - name: deb http://overviewer.org/debian ./
    - gpgcheck: 1
    - key_url: http://overviewer.org/debian/overviewer.gpg.asc
  pkg.installed:
    - name: minecraft-overviewer
