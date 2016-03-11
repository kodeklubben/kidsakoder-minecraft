flask_app:
  git.latest:
    - name: {{ pillar['flask_app']['git_repo'] }}
    - branch: {{ pillar['flask_app']['git_branch'] }}
    - target: {{ pillar['flask_app']['srv_dir'] }}
