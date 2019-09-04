#!/usr/bin/env python

import rospy
import cmdMotores
import cmdGarras
from std_msgs.msg import Int32MultiArray, Int16
from byakugan.msg import CtrlMotores, BoolStamped, SensoresDistanciaMsg, BoolGarras
import message_filters
import time

import rospy
class Resgate():
    def __init__(self):
        rospy.init_node("resgate", anonymous=False)

        self.pub = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10, latch=True)
        self.cmd = cmdMotores.CmdMotores(self.pub)

        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmdGarras = cmdGarras.CmdGarras(self.pubGarras)

        self.encontrou = False
        self.resgatou = False
        self.estouPerto = False

        self.executou = False

        subInit = message_filters.Subscriber('initResgatar', BoolStamped)
        subCentroid = message_filters.Subscriber('centroid_rectangle', BoolStamped)
        subSonar = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

        ts = message_filters.TimeSynchronizer([subInit, subCentroid, subSonar], 20)
        ts.registerCallback(self.callback)

    def callback(self, init, areaBool, sonar):
        if init.existe.data and not self.executou:
            if self.encontrou and not self.resgatou:
                if sonar.sensoresDistancia[0] < 6:
                    self.resgatou = True
                    self.cmd.roboParar(0.8)
                    self.cmdGarras.resgatar()
                    self.executou = True
                else:
                    self.cmd.roboAcionarMotores(30, 34)
            else:
                if areaBool.existe.data == False:
                    rospy.loginfo("cade a tete?")
                    self.cmd.roboAcionarMotores(25, -25)
                else:
                    if areaBool.centroid.data > 30: # area na esq
                        #self.publishLeds(1, 0, 0)
                        rospy.loginfo("area na esq")
                        self.cmd.roboAcionarMotores(-25, 25)
                        #pass
                    elif areaBool.centroid.data < -50: # area na dir
                        #self.publishLeds(0, 0, 1)
                        rospy.loginfo("area na dir")
                        self.cmd.roboAcionarMotores(25, -25)
                        #pass
                    elif not self.encontrou:
                        rospy.loginfo("achei a tete!!!")
                        self.encontrou = True
                        self.cmd.roboParar(1)
        else:
            rospy.loginfo('resgatei a tete')


if __name__ == "__main__":
    node = Resgate()
    rospy.spin()
