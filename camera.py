import cv2
from time import time
import numpy as np
from PIL import Image


class Camera(object):
    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    def get_frame(self):
        return self.frames[int(time()) % 3]


class VideoCamera(object):
    def __init__(self):
        

        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('./static/video/1.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


        cap = self.video
        ret, img = cap.read()
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
        success = ret
        #success, image = im.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        #return self.video