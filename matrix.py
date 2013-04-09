#!/usr/bin/python
from flask import Flask
from flask import render_template, request, Response
from flask import redirect, url_for
from functools import wraps
from imp import load_source
from os import listdir
from time import sleep
app = Flask(__name__)

def check_auth(username, password):
    return username == 'root' and password == 'h4ckit'

def authenticate():
    return Response(
       'Sorry, kid. You got the gift, but it looks like you\'re waiting for something.', 401,
       {'WWW-Authenticate': 'Basic realm="Neo... follow the white rabbit"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def all_services():
    return [i[:-3] for i in listdir("/opt/matrix/service/") if i[-2:]=='py' and i!='__init__.py']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/service')
@requires_auth
def service_list():
    services = all_services()

    service_table = {}
    
    for service in services:
        py_mod = load_source(service, '/opt/matrix/service/'+str(service)+'.py')
        service_table[service] = {
		'name': service, 
		'info': py_mod.info(), 
		'status': py_mod.status()['msg'],
		'css': py_mod.status()['type'],
	}
    
    return render_template('service_list.html',services=service_table)

@app.route('/service/<name>')
def service_status(name):
    if name in all_services():
        py_mod = load_source(name, '/opt/matrix/service/'+str(name)+'.py')
	info = py_mod.info()
	status = py_mod.status()
    else:
        info = 'error'
        status = 'not a valid service'
    return 'Info: %s<br>Status: %s' %(info,status)

@app.route('/service/<name>/<param>')
def service_action(name,param):
    if name in all_services():
        py_mod = load_source(name, '/opt/matrix/service/'+str(name)+'.py')
        if param=='start':
    	    msg = py_mod.start()
            sleep(0.3)
        if param=='stop':
            msg = py_mod.stop()
            sleep(0.5)
        if param=='info':
            msg = py_mod.info()
        if param=='status':
            msg = py_mod.status()
    else:
        msg = 'not a valid service'
    return redirect(url_for('service_list'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
