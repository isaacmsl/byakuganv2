#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray
from identificador import Detect

def callback(data):
	identificador = Detect(data)
		
	detectados = identificador.elementos_face('lbpcascades/lbpcascade_frontalface.xml')
	
	if (detectados is not None):
		for (x,y,w,h) in detectados:
			arrayCoordenadas.data[0] = x
			arrayCoordenadas.data[1] = y
			arrayCoordenadas.data[2] = w
			arrayCoordenadas.data[3] = h

			publicarCoordenadas(arrayCoordenadas)
	else:
		publicarCoordenadas(arrayCoordenadasAnt)


def publicarCoordenadas(coordenadas):
	pub = rospy.Publisher('coordenadas_detectadas', Float64MultiArray, queue_size=10)
	rate = rospy.Rate(10)
	pub.publish(coordenadas)
	rate.sleep()

def listenerImg():
	rospy.init_node('talkerCoordenadasFaces', anonymous=True)
	rospy.Subscriber('topico_img', Image, callback)
	rospy.spin()

if __name__ == "__main__":
	arrayCoordenadas = Float64MultiArray()
	arrayCoordenadas.data = [0,0,0,0]
	
	arrayCoordenadasAnt = Float64MultiArray()
	arrayCoordenadasAnt.data = [0,0,0,0]
	listenerImg()
