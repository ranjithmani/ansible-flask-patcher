# ansible-flask-patcher

API based ansible patching implemented using Flask.

## features

- API Based patching
- Authentication and host restriction 
- Logging 
- Reporting 


## limitations 

- Only take one server at a time
- Patching status will not be reported
- Reporting capabilities are limited 


## Usage

```
export FLASK_APP=patch.py
export FLASK_DEBUG=True
flask run
```
