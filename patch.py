from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from datetime import datetime
import os
import logging 
import platform
import subprocess

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://172.17.0.2:27017/patch"
mongo = PyMongo(app)
patch_collection = mongo.db.patch
logging.basicConfig(filename='patch.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
inv = ['node1', 'node2', 'node3', 'node4']
user = ['user']

@app.route('/patch/<fqdn>/<uid>')
def patch(fqdn, uid):
    now = datetime.now()
    format = "%d-%m-%y-%H:%M:%S"
    time = now.strftime(format)
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', fqdn]
    if fqdn not in inv:
        app.logger.error('Error level log')
        retJson = {
                "Server": fqdn,
                "Status": 'NotPermitted'
                }
        patch_collection.insert_one({"time": time, "user": uid, "server": fqdn, "status": 'NotPermitted'})
        return jsonify(retJson)
    if uid not in user:
        retJson = {
                "Server": fqdn,
                "Status": 'Unauthorized'
                }
        patch_collection.insert_one({"time": time, "user": uid, "server": fqdn, "status": 'Unauthorized'})
        return jsonify(retJson)
    if subprocess.call(command) != 0:
        retJson = {
                "Server": fqdn,
                "State": 'Unreachable',
                "Patch_Status": 'NotInitiated'
                }
        patch_collection.insert_one({"time": time, "user": uid, "server": fqdn, "status": 'Unreachable'})
        return jsonify(retJson)
    else:
        cmd = "ansible-playbook -i %s, patch-linux.yml &" %fqdn
        os.system(cmd)
        app.logger.info('Info level log')
        retJson = {
                "Server": fqdn,
                "State": 'Reachable',
                "Patch_Status": 'Initiated'
                }
        patch_collection.insert_one({"time": time, "user": uid, "server": fqdn, "status": 'Patch_initiated'})
        return jsonify(retJson)


@app.route('/patch/report')
def report():
    rep = (patch_collection.find({}))
    return render_template('report.html', report = rep)

@app.route('/patch/report/<fqdn>')
def reportf(fqdn):
    server = patch_collection.find({'server' : fqdn})
    return render_template('report.html', report = server)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
