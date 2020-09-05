from sys import stdout
import logging
from flask_socketio import SocketIO
from flask import Flask, render_template, Response, stream_with_context, request, redirect
from PIL import Image
from flask_socketio import SocketIO
import os
import io
import base64
import cv2
import time
import numpy as np

app = Flask(__name__)

PATH_TO_TEST_IMAGES_DIR = './images'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


@app.route('/submit',methods=['POST'])
def submit():
	img = request.files['image']  # get the image
	f = ('%s.jpg' % time.strftime("%Y%m%d-%H%M%S"))
	img.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))		
	
	return Response("%s saved" % f)


def gen():
	while True:
		try:
			a = os.listdir('./images')
			cap = cv2.imread("./images/"+ a[-1])
		except:
			cap = cv2.imread("./static/img/1.jpg")

		img = cap

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		image = img

		ret, jpeg = cv2.imencode('.jpg', image)

		frame = jpeg.tobytes()

		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/video_feed')

def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')

def index():
    return render_template('index2.html')



if __name__ == '__main__':
	#app.run(host="192.168.1.112", port=int(os.environ.get("PORT", 8080)), debug=True)
	app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)
	#app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
	#socketio.run(app,host="0.0.0.0", port=int(os.environ.get("PORT", 5000))
