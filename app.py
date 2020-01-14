from sys import stdout
import logging
from flask_socketio import SocketIO
from flask import Flask, render_template, Response, stream_with_context, request, redirect
from PIL import Image
from camera import VideoCamera
from flask_socketio import SocketIO
import os
import io
import base64
import cv2
import time
import numpy as np

app = Flask(__name__)

PATH_TO_TEST_IMAGES_DIR = './images'


@app.route('/submit',methods=['POST'])
def submit():


	img = request.files['image']  # get the image
	f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
	img.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR, f))		
	
	return Response("%s saved" % f)

'''
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
'''
def gen(camera):
	while True:
		a = os.listdir('./images')

		frame = Image.open("./images/"+ a[-1]).tobytes()
		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
@app.route('/feed')
def video_feed():
    return Response(img, mimetype='multipart/x-mixed-replace; boundary=frame')
'''



@app.route('/')
def index():

    return render_template('index2.html')


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)
	#socketio.run(app,host="0.0.0.0", port=int(os.environ.get("PORT", 5000))
