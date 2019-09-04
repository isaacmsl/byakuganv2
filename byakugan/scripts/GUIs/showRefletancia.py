#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import message_filters
from std_msgs.msg import Float64MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg

def callbackRefle(refle):
    if(len(refle.refletancia) > 0):
        valorSensor = refle.refletancia
        rospy.loginfo('refletancia: ' + str(valorSensor))

        show = np.zeros((150,600,3), np.uint8)
        #show = cv2.resize(show, (600, 150))

        w = show.shape[1]
        h = show.shape[0]
        cor = (0,0,0)

        show = cv2.rectangle(show, (w,h), (0,0), (255,255,255),-1)

        for i in range(1, 4):
            pt1 = (i*w/4, 0)
            pt2 = (i*w/4, h)
            show = cv2.line(show, pt1, pt2, cor)

        for i in range(0, 4):
            valorSensor = refle.refletancia[i]
            if(valorSensor < 4):
                pt1 = (i*w/4, 0)
                pt2 = ((i+1)*w/4, h)
                show = cv2.rectangle(show, pt1, pt2, (0,0,0), -1)

        cv2.imshow('cor', show)
        cv2.waitKey(1)

def listenerRefletancia():
    rospy.init_node('refletanciaGUI', anonymous=True)
    subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
    subRefle.registerCallback(callbackRefle)

    rospy.spin()

if __name__ == "__main__":
	try:
		listenerRefletancia()
	except rospy.ROSInterruptException:
		pass
