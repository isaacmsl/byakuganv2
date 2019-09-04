#!/usr/bin/env python

import rospy
import cv2
import message_filters
import numpy as np
from std_msgs.msg import Float64MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg

def callbackDistancia(data):
    if(len(data.sensoresDistancia) > 0):
        valorSensor = data.sensoresDistancia[0]
        rospy.loginfo('sonar: ' + str(valorSensor))

        show = np.zeros((500,500,3), np.uint8)
        #show = cv2.resize(show, (500, 500))

        w = show.shape[1]
        h = show.shape[0]

        raio = map(valorSensor, 1, 40, w/2, 1)
        centro = (w/2, h/2)

        show = cv2.circle(show, centro, int(raio), (0,255,0), -1)

        show = cv2.putText(show, str(valorSensor),(w/2,h/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

        cv2.imshow('distancia', show)
        cv2.waitKey(1)

def map(x, in_min, in_max, out_min, out_max):
    if (x > in_max):
        x = in_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def listenerDistancia():
    rospy.init_node('distanciaGUI', anonymous=True)
    subSonar = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
    subSonar.registerCallback(callbackDistancia)

    rospy.spin()

if __name__ == "__main__":
	try:
		listenerDistancia()
	except rospy.ROSInterruptException:
		pass
