#!/usr/bin/env python
import rospy
import numpy
import os
import message_filters
import time
import cmdMotores
import cmdGarras
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores

class Sala3():
    def __init__(self):
        rospy.init_node("sala3", anonymous=False)

        self.podeExecutar = False
        self.executou = False

        # procurar things
        self.encontrou = False
        self.encontrouArea = False
        self.pegou = False
        self.resgatou = False

        self.entrouNaSala = False

        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmdGarras = cmdGarras.CmdGarras(self.pubGarras)

        self.pubMotores = rospy.Publisher('cmdMotores', CtrlMotores , queue_size=10, latch=True)
        self.cmdMotores = cmdMotores.CmdMotores(self.pubMotores)
        

        subBtns = message_filters.Subscriber('botoes_init', BotoesMsg)
        subBall = message_filters.Subscriber('tem_circulos', BoolStamped)
        subCoordinates = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        subDist = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
        subCentroid = message_filters.Subscriber('centroid_rectangle', BoolStamped)

        ts = message_filters.TimeSynchronizer([subBtns, subCoordinates,subBall, subDist, subCentroid], 20)
        ts.registerCallback(self.callback)
    
    def callback(self, btns, coordinates, circle, dist, centroid):
        if btns.botao2.data:
            self.podeExecutar = True
        elif btns.botao3.data:
            self.podeExecutar = False
            self.executou = False
        
        if self.podeExecutar and not self.executou:
            if not self.encontrou:
                self.procurar(coordinates, circle, dist)
            if self.encontrou and not self.pegou:
                self.pegar(coordinates)
            elif self.pegou and not self.resgatou:
                self.resgatar(centroid, dist)
            elif self.encontrou and self.pegou and self.resgatou:
                self.executou = True
    
    def procurar(self, coordinates, circle, dist):
        x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

        if(self.entrouNaSala):
            if circle.existe.data:
                self.encontrou = True
                
                if self.encontrou:
                    self.cmd.roboAcionarMotores(0, 0)
                    
                    rospy.loginfo("achei a tete")
                    
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

    def pegar(self, coordinates):
        x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z

        if(r < 48 and self.encontrei == False ):
            rospy.loginfo("Estou longe")
            self.cmdMotores.roboAcionarMotores(30, 34)
        else:
            self.cmdMotores.roboAcionarMotores(0,0)
            rospy.loginfo("Estou perto")

            self.cmdGarras.abrirMao()
            self.cmdGarras.abaixarBraco()
            self.cmdGarras.fecharMao()
            self.cmdGarras.subirBraco()
            time.sleep(2)
            self.pegou = True

    def resgatar(self):
        if self.encontrouArea and not self.resgatou:
            if sonar.sensoresDistancia[0] < 6:
                self.resgatou = True
                self.cmd.roboParar(0.8)
                self.cmdGarras.resgatar()
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
                    self.encontrouArea = True
                    self.cmd.roboParar(1)


if __name__ == "__main__":
    node = Sala3()
    rospy.spin()