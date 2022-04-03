# ansible-flask-patcher

API based ansible patching implemented using Flask.

## features

- API Based patching
- Authentication and host restriction 
- Logging 
- Reporting 
- API requests are stored in mongodb 


## limitations 

- Only take one server at a time
- Patching status will not be reported
- TLS not implemented. 


## Usage

```
export FLASK_APP=patch.py
export FLASK_DEBUG=True
flask run
```
use curl or any browser to initiate patching 
```
curl http://127.0.0.1:5000/patch/<server>/username
server   => provide FQDN and the server should be reahable and ansible connectivity configured
username => provide user name that configured for the patching
```

To get the repotrs, use curl or any browser to initiate patching.

```
curl http://127.0.0.1:5000/patch/report 
the above command will print all the reports 

curl http://127.0.0.1:5000/patch/report/<server>
server => fqdn of the server name that you are looking for the report.
