from sys import stdout
import logging
from flask_socketio import SocketIO
from flask import Flask, render_template, Response, stream_with_context, request
from PIL import Image
from camera import VideoCamera
from flask_socketio import SocketIO
import os
import io
import base64
import cv2
import numpy as np


app = Flask(__name__)
socketio = SocketIO(app)


def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/submit',methods=['POST','GET'])
def submit():
	image = request.args.get('image')
	#dosya = open("deneme.txt","w")
	#dosya.write(image)
	#dosya.close
	return render_template('index2.html')

	
@app.route('/')
def index():
    return render_template('index2.html')


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8080)), debug=True)
	#socketio.run(app,host="0.0.0.0", port=int(os.environ.get("PORT", 5000))
