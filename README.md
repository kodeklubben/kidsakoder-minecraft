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
To run Flask locally on ```http://localhost:5000```, run the following:
```
python runserver.py
```

## Coding conventions
#### Branch naming
```
feat/       Features
bugfix/     Bug fixes
exp/        Experimental
(If using / in repo name, waffle will interpret as cross repo reference and not move issue automatically)
```

##### Examples
```
feat/add-flask-#33          A new feature branch for adding Flask in issue #33
bugfix/typo-in-header-#21   A bug fix branch to fix a typo in issue #21
exp/testing-mysql           An experimental branch for testing my-sql
```
