apache2:
  pkg:
    - installed
  service.running:
    - watch:
      - pkg: apache2
