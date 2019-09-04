#!/usr/bin/env python
import rospy
import numpy
import os
import message_filters
import cmdMotores
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores

class FindBalls:
    def __init__(self):
        rospy.init_node("findBalls", anonymous=False)

        self.achouVitima = False
        self.executou = False
        self.entrouNaSala = False
        self.podeExecutar = False

        self.qntAchou = 0

        self.pubMotores = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10)
        self.pubPegar = rospy.Publisher("initPegar", BoolStamped, queue_size=10, latch=True)    

        self.cmd = cmdMotores.CmdMotores(self.pubMotores)
        subCoordinates = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        subBall = message_filters.Subscriber('tem_circulos', BoolStamped)
        subDist = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
        subBtns = message_filters.Subscriber('botoes', BotoesMsg)

        ts = message_filters.TimeSynchronizer([subCoordinates, subBall, subDist, subBtns], 20)
        ts.registerCallback(self.ballsCb)

    def initPegar(self):
        initData = BoolStamped()
        initData.existe.data = True
        self.pubPegar.publish(initData)
        self.executou = True

    def ballsCb(self, coordinates, circle, dist, btns):
        if btns.botao2.data:
            self.podeExecutar = True
    
        if self.podeExecutar:
            if self.executou == False:
                x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

                if(dist.sensoresDistancia[2] > 10):
                    self.entrouNaSala = True

                if(self.entrouNaSala):
                    if circle.existe.data:
                        self.achouVitima = True
                        
                        if self.achouVitima:
                            self.cmd.roboAcionarMotores(0, 0)
                            
                            rospy.loginfo("achei a tete")
                            #self.executou = True
                            #self.initPegar()

                            '''
                            if x in numpy.arange(200, 280, 1):
                                self.cmd.roboAcionarMotores(0, 0)
                                self.pegarVitima()
                            '''
                    else:
                        '''
                        if not self.qntAchou < 0:
                            self.qntAchou = self.qntAchou - 1
                        else:
                            self.qntAchou = 0

                        rospy.loginfo("cade a tete")
                        '''
                        self.cmd.roboAcionarMotores(-30, 30)
                else: 
                    rospy.loginfo("rampa")
                    self.cmd.roboAcionarMotores(50, 54)
            else:
                self.initPegar()

if __name__ == "__main__":
    node = FindBalls()
    rospy.spin()
