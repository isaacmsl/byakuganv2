#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import BoolStamped

def dispo(img, circles):
	if (circles is not None):
		circles = np.uint16(np.around(circles))
		circulo.existe.data = True
		maiorRaio = 0
		for i in circles[0, :]:
			x, y, r = i[0], i[1], i[2]

			if(r > maiorRaio):
				maiorRaio = r
				coordenadas.vector.x = x
				coordenadas.vector.y = y
				coordenadas.vector.z = r
	else:
		circulo.existe.data = False

		coordenadas.vector.x = 0
		coordenadas.vector.y = 0
		coordenadas.vector.z = 0

	pub.publish(coordenadas)
	pub2.publish(circulo)

def pubCirculosEm(img):
	copiaImg = img.copy()

	cinza = cv2.cvtColor(copiaImg, cv2.COLOR_BGR2GRAY)
	cinza = cv2.medianBlur(cinza, 5)

	rows = cinza.shape[1]

 	circles = cv2.HoughCircles(cinza, cv2.HOUGH_GRADIENT, 1.2, rows/8,
 		param1=45, param2=30, minRadius=10, maxRadius=100)

	dispo(copiaImg, circles)

def callback(img):

	np_arr = np.fromstring(img.data, np.uint8)
	imgCV = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

	pubCirculosEm(imgCV)
	'''
	imgCV = ponte.imgmsg_to_cv2(img, 'bgr8')
	pubCirculosEm(imgCV)
	cv2.imshow('img', imgCV)
	cv2.waitKey(1)
	'''

def listenerImg():
	rospy.init_node('pubCircle', anonymous=False)
	rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, callback)
	#rospy.Subscriber("imgCam", Image, callback)

	rospy.spin()

if __name__ == "__main__":
	ponte = CvBridge()

	pub = rospy.Publisher('coordenadas_circulos', Vector3Stamped, queue_size=10)
	pub2 = rospy.Publisher('tem_circulos', BoolStamped, queue_size=10)

	circulo = BoolStamped()
	coordenadas = Vector3Stamped()
	listenerImg()
