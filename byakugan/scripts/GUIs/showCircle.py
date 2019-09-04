#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import message_filters
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import BoolStamped

def desenharCirculos(img, coordenadas):
    x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z
    copiaImg = img.copy()

    center = (x, y)
    radius = r

    cv2.circle(copiaImg, center, 1, (0,100,100), 3) #centro
    cv2.circle(copiaImg, center, radius, (255, 0, 255), 3) #borda

    return copiaImg

def callback(img, coordenadas):
	np_arr = np.fromstring(img.data, np.uint8)
	imgCV = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

	imgCV = cv2.flip(imgCV, 2)

	#imgCV = desenharCirculos(imgCV, coordenadas)

	cv2.namedWindow('LISTENER_1', cv2.WINDOW_NORMAL)
	cv2.imshow('LISTENER_1', imgCV)
	cv2.waitKey(1)

def listenerImg():
    rospy.init_node('showCircle', anonymous=True)

    subCompImg = message_filters.Subscriber('/raspicam_node/image/compressed', CompressedImage)
    subCoordenadas = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)

    ts = message_filters.TimeSynchronizer([subCompImg, subCoordenadas], 20)

    ts.registerCallback(callback)

    rospy.spin()

if __name__ == "__main__":
	circulo = BoolStamped()
	listenerImg()
