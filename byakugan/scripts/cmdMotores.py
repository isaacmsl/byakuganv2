#!/usr/bin/env python

import rospy
from byakugan.msg import CtrlMotores

class CmdMotores():
    def __init__(self, pub):
        self.pubMotores = pub
        self.dataMotores = CtrlMotores()

    def roboAcionarMotores(self, esq, dir, delay=0):
        if esq < 100 and dir < 100:
            self.dataMotores.esq.data = esq
            self.dataMotores.dir.data = dir
            self.dataMotores.delay.data = delay
            self.pubMotores.publish(self.dataMotores)
            rospy.loginfo("[PUBLISHED] roboAcionarMotores!")

    def roboEmFrente(self, delay=0):
        self.dataMotores.esq.data = 1
        self.dataMotores.dir.data = 1
        self.dataMotores.delay.data = delay
        self.pubMotores.publish(self.dataMotores)
        rospy.loginfo("[PUBLISHED] roboEmFrente!")
    def roboEsq(self, delay=0):
        self.dataMotores.esq.data = -1
        self.dataMotores.dir.data = 1
        self.dataMotores.delay.data = delay
        self.pubMotores.publish(self.dataMotores)
        rospy.loginfo("[PUBLISHED] roboEsq!")
    def roboDir(self, delay=0):
        self.dataMotores.esq.data = 1
        self.dataMotores.dir.data = -1
        self.dataMotores.delay.data = delay
        self.pubMotores.publish(self.dataMotores)
        rospy.loginfo("[PUBLISHED] roboDir!")
    def roboParaTras(self, delay=0):
        self.dataMotores.esq.data = -1
        self.dataMotores.dir.data = -1
        self.dataMotores.delay.data = delay
        self.pubMotores.publish(self.dataMotores)
        rospy.loginfo("[PUBLISHED] roboParaTras!")
    def roboParar(self, delay=0):
        self.dataMotores.esq.data = 0
        self.dataMotores.dir.data = 0
        self.dataMotores.delay.data = delay
        self.pubMotores.publish(self.dataMotores)
        rospy.loginfo("[PUBLISHED] roboParar!")
