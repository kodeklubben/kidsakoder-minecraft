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

{% endfor %}
