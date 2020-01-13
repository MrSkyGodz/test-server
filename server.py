import os
from hashlib import *
from bottle import Bottle,route,static_file,run,template,request,get,post
import json
import numpy as np

global ips
global click
ips = []

click = {
  "ips": 0
}
del click["ips"]

def home_page():
	click = ip()
	

	l1 = []
	l2 = []
	for i in click:
		l1.append(i)
	for i in click:
		l2.append(click[i])


	return template("./weppage/index.html",a = l1,b = l2)
def edu_page():
	return template("./weppage/isimsize.html")

def contacts_page():
	return template("./weppage/isimsizc.html")

def career_page():
	return template("./weppage/isimsizcr.html")

def source_page():
	return template("./weppage/isimsizs.html")


@route("/static/<filename>")
def server_static(filename):
	return static_file(filename, root='./weppage')

@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='./weppage')


def ip():
    your_ip = request.environ.get('REMOTE_ADDR')
	#your_ip = request.headers.get("X-Forwarded-For", "127.0.0.1")

    if your_ip in ips:
    	click[your_ip] += 1
    else:
    	ips.append(your_ip)
    	click[your_ip] = 1
	#return ["{}".format(your_ip)]
    return click

def ip_restart():
	 click.clear()
	 ips.clear()

	
    

admin_hash ='dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91'
#dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91
 
def create_hash(password):
    str(password).encode() 
    return sha256( str(password).encode()).hexdigest()

def password():

    p = request.POST.get("password")
    hsh1 = create_hash(p)
    if admin_hash == hsh1:
         ip_restart()
    
    return home_page()#["{}".format(hsh1)]   # return  ["asdasdasd"]

def open(app):
	app.route("/", "GET", home_page)
	app.route("/index.html", "GET", home_page)
	
	app.route("/static/<filename>", "GET", server_static)
	app.route("/static/<filename:path>", "GET", static)

	app.route("/isimsize.html", "GET", edu_page)
	app.route("/isimsizcr.html", "GET", career_page)
	app.route("/isimsizc.html", "GET", contacts_page)
	app.route("/isimsizs.html", "GET", source_page)
	

	app.route("/ip", "GET", ip)

	app.route('/password', "POST",password )


   
def create_app():
	app = Bottle()
	open(app)
	return app


application = create_app()
application.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))


#if __name__ == '__main__':
#	run(reloader=True, debug=True,host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))