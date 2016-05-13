# This state adds users defined in the users Pillar and removes the default user used for provisioning

# Go through users in the users Pillar and make sure they are present
{% for user, args in pillar['users'].iteritems() %}

{{ user }}:
  user.present:
    - name: {{ args['name'] }}
    - shell: {{ args['shell'] }}
    - password: {{ args['password'] }}
  {% if 'groups' in args %}
    - groups: {{ args['groups'] }}
  {% endif %}

{% if args['ssh-keys'] %}
{{ user }}_key:
  ssh_auth.present:
    - user: {{ args['name'] }}
    - names:
      {% for key in args['ssh-keys'] %}
      - {{ key }}
      {% endfor %}
{% endif %}

{% endfor %}
