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
First you need a config file with location for the database and a secret key.
Create any plain text file with:
```
DATABASE='path/to/database.db' # Folders need to be created
SECRET_KEY='development key' # this can be anything
```
Then run set the variable in a unix console with:
```
export APP_SETTINGS='settings.config'
```
Then the database needs to be initialized. Start a python prompt:
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
feat/       Features
bugfix/     Bug fixes
exp/        Experimental
```

##### Examples
```
feat/add-flask-#33          A new feature branch for adding Flask in issue #33
bugfix/typo-in-header-#21   A bug fix branch to fix a typo in issue #21
exp/testing-mysql           An experimental branch for testing my-sql
```
