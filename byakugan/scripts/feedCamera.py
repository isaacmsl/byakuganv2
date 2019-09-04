#!/usr/bin/env python
'''
doc:
	uso para multi-thread
autor:
	paulovlb
'''

import rospy
import threading
import message_filters
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import BoolStamped
from camera import Camera

class FeedCamera(Camera):
    def __init__(self):
        Camera.__init__(self)
        self.subCoordenadas = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        self.subVitima = message_filters.Subscriber('tem_circulos', BoolStamped)
        
    def register(self):
        self.ts = message_filters.TimeSynchronizer([self.subCoordenadas, self.subVitima], 20)
        self.ts.registerCallback(self.camCallback)
        
    def camCallback(self, coordenadas, vitima):
        #rospy.loginfo(vitima.existe.data)
        self.setValues(coordenadas, vitima)
 
        
