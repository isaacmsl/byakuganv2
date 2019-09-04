#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from std_msgs.msg import Float64MultiArray
from byakugan.msg import BoolStamped

def circular(img, circles):
	if (circles is not None):
		circles = np.uint16(np.around(circles))
		maiorRaio = 0
		midColor = 0
		for i in circles[0, :]:
			x, y, r = i[0], i[1], i[2]

			center = (x, y)
			radius = r

			if(radius > maiorRaio):
				midColor = 255
				maiorRaio = r
			else:
				midColor = 0

			cv2.circle(img, center, 1, (0,100,100), 3) #centro
			cv2.circle(img, center, radius, (255, midColor, 255), 3) #borda
	return img

def acharCirculos(img):
	copiaImg = img.copy()

	cinza = cv2.cvtColor(copiaImg, cv2.COLOR_BGR2GRAY)
	cinza = cv2.medianBlur(cinza, 5)

	rows = cinza.shape[1]

 	circles = cv2.HoughCircles(cinza, cv2.HOUGH_GRADIENT, 1.2, rows/8,
 		param1=100, param2=30, minRadius=10, maxRadius=100)

	copiaImg = circular(copiaImg, circles)

	return copiaImg

def callback(img):
	np_arr = np.fromstring(img.data, np.uint8)
	imgCV = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

	imgCV = cv2.flip(imgCV, 2)

	imgCV = acharCirculos(imgCV)

	cv2.namedWindow('SHOW_DE_BOLA', cv2.WINDOW_NORMAL)
	cv2.imshow('SHOW_DE_BOLA', imgCV)
	cv2.waitKey(1)

def listenerImg():
	rospy.init_node('showAllCircles', anonymous=True)
	rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, callback)
	rospy.spin()

if __name__ == "__main__":
	circulo = BoolStamped()
	arrayCoordenadas = Float64MultiArray()
	arrayCoordenadas.data = [0,0,0]

	listenerImg()
