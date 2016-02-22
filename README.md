kidsakoder-minecraft
====================

## How to run 
#### Requirements
First, make sure you have ```Python``` and ```pip``` installed.

To install Flask and any other requirements, run the following:
```
pip install -r requirements.txt
```

#### Running Flask locally
To run Flask locally on ```http://localhost:5000```, you need to do the following:

Generate a secret key by running the following in the ```flask_app``` folder:
```
python gen_secret_key.py
```
Then the database needs to be initialized. Start a python prompt in the root repository folder:
```
python
```
In the prompt run:
```
>>> from flask_app.database import init_db
>>> init_db()
```
Then start the server by running:
```
python runserver.py
```

## Coding conventions
#### Branch naming
```
feat_       Features
bugfix_     Bug fixes
exp_        Experimental
(If using / in branch name, waffle will interpret as cross repo reference and not move issue automatically)
```
#### Pull requests
When creating pull requests, use the keyword 'closes' to group with issue in waffle.
```
feat_add-flask closes #33
```
##### Examples
```
feat_add-flask-#33          A new feature branch for adding Flask in issue #33
bugfix_typo-in-header-#21   A bug fix branch to fix a typo in issue #21
exp_testing-mysql           An experimental branch for testing my-sql
```
