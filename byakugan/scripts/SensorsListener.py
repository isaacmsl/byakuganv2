#!/usr/bin/env python

import rospy
import threading
import message_filters
from Sensores import Sensores
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BotoesMsg

class SensorsListener(Sensores):
    def __init__(self):
        Sensores.__init__(self)
        self.subBotoes = message_filters.Subscriber('botoes', BotoesMsg)
        self.subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
        self.subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

    def register(self):
        self.ts = message_filters.TimeSynchronizer([self.subRefle, self.subDistancia, self.subBotoes], 20)
        self.ts.registerCallback(self.sensorsCallback)
        rospy.spin()
    def sensorsCallback(self, refle, dist, btns):
        #rospy.loginfo("oi")
        self.setValues(refle, dist, btns)
