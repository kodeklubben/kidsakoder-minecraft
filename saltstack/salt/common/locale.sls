### Locale and time
# Make sure Norwegian locale is available
norwegian-locale:
  locale.present:
    - name: nb_NO.UTF-8

# Set Norwegian timezone
norwegian-timezone:
  timezone.system:
    - name: Europe/Oslo
