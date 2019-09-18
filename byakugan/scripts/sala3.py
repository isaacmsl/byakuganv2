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

    def PROCURAR(self): return 0
    def PEGAR(self): return 1
    def RESGATAR(self): return 2
    def RETORNAR(self): return 3

    def __init__(self):
        rospy.init_node("sala3", anonymous=False)

        self.podeExecutar = False
        self.executou = False

        self.estadoRobo = 0
        self.estadoPegar = 0
        self.pediuReset = False
        self.estadoResgatar = 0
        self.estadoArea = 0
        self.logIndex = 0

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

        cliqBtn1 = btns.botao2.data
        cliqBtn3 = btns.botao3.data

        if cliqBtn1 and not self.pediuReset: # primeira execucao
            rospy.logwarn("Posso executar;")
            self.podeExecutar = True
        elif cliqBtn3 and not self.pediuReset: # pede reset e para execucao
            rospy.logwarn("Parei porque pediram reset;")
            self.pediuReset = True
            self.podeExecutar = False
        elif cliqBtn1 and self.pediuReset: # reseta execucao
            rospy.logwarn("Resetando execucao;")
            self.podeExecutar = True # permite execucao inicial
            self.pediuReset = False
            # self.resetVars() ?

        if self.podeExecutar:
            if self.estadoRobo == self.PROCURAR():
                if self.logIndex == 0:
                    self.logIndex = 1
                    rospy.logwarn("Estou procurando!;")

                self.procurar(coordinates, circle, dist)
            elif self.estadoRobo == self.PEGAR():
                if self.logIndex == 1:
                    self.logIndex = 2
                    rospy.logwarn("Vou pegar!;")

                self.pegar(coordinates)
            elif self.estadoRobo == self.RESGATAR():
                if self.logIndex == 2:
                    self.logIndex = 3
                    rospy.logwarn("Resgatando...;")

                self.resgatar(centroid, dist)
            elif self.estadoRobo == self.RETORNAR():
                rospy.logwarn("Salvei a vitima!;")
                #self.executou = True
        '''
        elif self.podeExecutar and self.executou:
            self.cmdMotores.roboParaTras(1)
            self.cmdMotores.roboDir(1)
            self.cmdMotores.roboParar(1)
            self.reboot()
        '''
    def resetVars(self):
        self.estadoRobo = 0
        '''
        self.encontrou = False
        self.encontrouArea = False
        self.pegou = False
        self.resgatou = False
        self.chegueiPerto = False
        self.entrouNaSala = False
        '''

    def procurar(self, coordinates, circle, dist):
        
        if not self.encontrou:
            x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

            if circle.existe.data:
                rospy.logwarn("Encontrei a vitima!;")
                self.encontrou = True
                self.cmdMotores.roboParar(1)
                rospy.logwarn("Parei;")
                self.estadoRobo = self.PEGAR()
                rospy.logwarn("Posicionado para pegar!;")
            else:
                rospy.loginfo("Nao estou encontrando...")
                self.cmdMotores.roboAcionarMotores(-30, 30)

    def zerarPegar(self):
        self.abriu = False
        self.fechou = False
        self.abaixou = False
        self.subiu = False

    def pegar(self, coordenadas):
        if self.estadoPegar == 0:
            x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z
            
            raioPequeno = y < 160

            if not raioPequeno:
                rospy.logwarn("Estou longe")
                self.cmdMotores.roboAcionarMotores(30, 32)
            else:
                self.estadoPegar = 1
        else:
            if self.estadoPegar == 1:
                self.cmdMotores.roboParar(1)
                rospy.logwarn("Parei;")
                self.estadoPegar = 2

            elif self.estadoPegar == 2:
                self.cmdMotores.roboEmFrente(1)
                rospy.logwarn("Fui um pouco pra frente!;")
                self.estadoPegar = 3

            elif self.estadoPegar == 3:
                self.cmdMotores.roboParar(1)
                rospy.logwarn("Parei novamente;")
                self.estadoPegar = 4
            
            elif self.estadoPegar == 4:
                self.cmdGarras.abrirMao()
                rospy.logwarn('Abri!')
                self.estadoPegar = 5

            elif self.estadoPegar == 5:
                self.cmdGarras.abaixarBraco()
                rospy.logwarn('Abaixei!')
                self.estadoPegar = 6

            elif self.estadoPegar == 6:
                self.cmdGarras.fecharMao()
                rospy.logwarn('Fechei!')
                self.estadoPegar = 7

            elif self.estadoPegar == 7:
                self.cmdGarras.subirBraco()
                rospy.logwarn('Subi!')
                self.estadoPegar = 8

            elif self.estadoPegar == 8:
                rospy.logwarn('Parei!')
                self.estadoPegar = 9
                self.cmdMotores.roboParar(1)
            
            elif self.estadoPegar == 9: # aproveita loop callback para demorar um pouco para comecar
                self.estadoRobo = self.RESGATAR()
            

    def resgatar(self, areaBool, dist):
        if self.estadoResgatar == 0:
            if areaBool.existe.data:
                self.cmdMotores.roboParar(1)
                rospy.logwarn('Encontrei a area!;')
                self.estadoResgatar = 1 # robo comecar a verificar
            else:
                rospy.logwarn("Procurando area...;")
                self.cmdMotores.roboAcionarMotores(25, -25)

        elif self.estadoResgatar == 1:
            if self.verificouArea: # area verifica true
                if dist.sensoresDistancia[0] < 8:

                    if self.estadoArea == 1:
                        self.cmdMotores.roboParar(2)
                        rospy.logwarn('Parei!')
                        self.estadoArea = 2

                    elif self.estadoArea == 2:
                        self.cmdGarras.resgatar()
                        rospy.logwarn('Resgatei!')
                        self.estadoArea = 3
                        self.estadoRobo = self.RETORNAR()
                else:
                    if self.estadoArea == 0:
                        rospy.logwarn('Indo ate a area...')
                        self.cmdMotores.roboAcionarMotores(34,34)
                        self.estadoArea = 1
            else:
                if areaBool.existe.data and self.qntVisu > 10:
                    self.verificouArea = True
                elif areaBool.existe.data:
                    self.qntVisu = self.qntVisu + 1
                elif not areaBool.existe.data:
                    self.estadoPegar = 0 # deixou de verificar
            
                
                


if __name__ == "__main__":
    node = Sala3()
    rospy.spin()