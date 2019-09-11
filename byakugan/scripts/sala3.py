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
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras

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

        # inits
        self.initPegar = False
        self.initResgatar = False

        self.entrouNaSala = False

        self.qntVisu = 0
        self.verificouArea = False

        self.abriu = False
        self.fechou = False
        self.abaixou = False
        self.subiu = False

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
            elif self.encontrou and not self.pegou:
                self.pegar(coordinates)
            elif self.pegou and not self.resgatou:
                self.resgatar(centroid, dist)
            elif self.encontrou and self.pegou and self.resgatou:
                self.executou = True
        '''
        elif self.podeExecutar and self.executou:
            self.cmdMotores.roboParaTras(1)
            self.cmdMotores.roboDir(1)
            self.cmdMotores.roboParar(1)
            self.reboot()
        '''
    def reboot(self):
        self.encontrou = False
        self.encontrouArea = False
        self.pegou = False
        self.resgatou = False
        self.chegueiPerto = False
        self.entrouNaSala = False

    def procurar(self, coordinates, circle, dist):
        x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

        if circle.existe.data:
            self.encontrou = True
            
            if self.encontrou:
                self.cmdMotores.roboAcionarMotores(0, 0)
                
                rospy.loginfo("achei a tete")
                self.cmdMotores.roboParar(1)
                self.cmdMotores.roboEmFrente(0.5)
                self.cmdMotores.roboParar(2)
                
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
            '''
            rospy.loginfo("sumiu?!")
            
            self.cmdMotores.roboAcionarMotores(-30, 30)

    def zerarPegar(self):
        self.abriu = False
        self.fechou = False
        self.abaixou = False
        self.subiu = False

    def pegar(self, coordenadas):
        if not self.pegou:
            x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z
            
            raioPequeno = y < 160

            if not raioPequeno:
                if self.initPegar: 
                    self.zerarPegar()
                else:
                    rospy.loginfo("Estou longe")
                    self.cmdMotores.roboAcionarMotores(30, 32)
            elif raioPequeno and not self.pegou:
                if not self.initPegar:
                    rospy.logwarn('Parei!')
                    self.cmdMotores.roboParar(1)
                    self.initPegar = True
                elif not self.abriu:
                    self.cmdGarras.abrirMao()
                    rospy.loginfo('Abri!')
                    self.abriu = True
                elif self.abriu and not self.abaixou:
                    self.cmdGarras.abaixarBraco()
                    rospy.loginfo('Abaixei!')
                    self.abaixou = True
                elif self.abaixou and not self.fechou:
                    self.cmdGarras.fecharMao()
                    rospy.loginfo('Fechei!')
                    self.fechou = True
                elif self.fechou and not self.subiu:
                    self.cmdGarras.subirBraco()
                    rospy.loginfo('Subi!')
                    self.subiu = True
                elif self.subiu:
                    self.cmdMotores.roboAcionarMotores(0,0)
                    rospy.loginfo('Parei!')
                    self.pegou = True
                    self.cmdMotores.roboParar(2)
                

    def resgatar(self, areaBool, dist):
        if self.encontrouArea and not self.resgatou:
            if self.verificouArea:
                if dist.sensoresDistancia[0] < 8:
                    rospy.logwarn('iniciando o pegar')
                    if not self.initResgatar:
                        self.cmdMotores.roboParar(2)
                        rospy.loginfo('Parei!')
                        self.initResgatar = True
                    elif not self.resgatou:
                        self.cmdMotores.roboParar(2)
                        self.cmdGarras.resgatar()
                        self.resgatou = True
                        rospy.loginfo('Resgatei!')
            else:
                if areaBool.existe.data and self.qntVisu > 10:
                    self.cmdMotores.roboAcionarMotores(34,34)
                    self.verificouArea = True
                elif areaBool.existe.data:
                    self.qntVisu = self.qntVisu + 1
                elif not areaBool.existe.data:
                    self.encontrouArea = False

        else:
            if areaBool.existe.data == False:
                rospy.loginfo("cade a tete?")
                self.encontrouArea = False
                self.qntVisu = 0
                self.cmdMotores.roboAcionarMotores(25, -25)
            else:
                self.cmdMotores.roboParar(1)
                self.encontrouArea = True
                rospy.loginfo('Encontrei a area!')
                


if __name__ == "__main__":
    node = Sala3()
    rospy.spin()