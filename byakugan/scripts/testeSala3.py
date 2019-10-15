#!/usr/bin/env python
import rospy
import cmdMotores
import cmdGarras
from controle import Controle
from std_msgs.msg import Empty, Int8
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras
from geometry_msgs.msg import Vector3Stamped

class TesteSala3:

    def __init__(self):
        rospy.init_node("sala3", anonymous=True)

        self.c = Controle()
        
        self.pediuReset = False
        self.podeExecutar = False

        self.estadoRobo = 0 # comeca procurando
        self.logIndex = 0

        self.indexVolta = 0

        self.encontrouBola = False
        self.estadoPegar = 0

        # resgate things 
        self.estadoResgatar = 0
        self.verificouArea = False
        self.estadoArea = 0
        self.qntVisu = 0
        
        self.pubMotores = rospy.Publisher('cmdMotores', CtrlMotores , queue_size=10, latch=True)
        self.cmdMotores = cmdMotores.CmdMotores(self.pubMotores)

        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmdGarras = cmdGarras.CmdGarras(self.pubGarras)

        rospy.Subscriber("ctrl", Empty, self.main)

        rospy.Subscriber('botoes_init', BotoesMsg, self.c.btnsCb)
        rospy.Subscriber("tem_circulos", BoolStamped, self.c.temCirculoCb)
        rospy.Subscriber("coordenadas_circulos", Vector3Stamped, self.c.coordenadasCirculoCb)
        rospy.Subscriber("distancia", SensoresDistanciaMsg, self.c.distanciaCb)
        rospy.Subscriber("centroid_rectangle", BoolStamped, self.c.retanguloCb)
        rospy.Subscriber("status_motores", Int8, self.c.statusMotores)
        rospy.Subscriber("status_garras", Int8, self.c.statusGarras)

    def PROCURAR(self): return 0
    def PEGAR(self): return 1
    def RESGATAR(self): return 2
    def RETORNAR(self): return 3

    def resgatar(self):
        
        areaBool = self.c.getCentroid()
        dist = self.c.getDistancia(0) # pega sonar frontal

        if self.estadoResgatar == 0:
            if areaBool.existe.data:
                if not self.c.motorIsBusy():
                    self.cmdMotores.roboParar(1)
                    rospy.logwarn('Encontrei a area!')
                    self.estadoResgatar = 1 # robo comecar a verificar
                else:
                    rospy.logwarn('Encontrei a area (ESPERANDO MOTOR)')
            else:
                if not self.c.motorIsBusy():
                    rospy.logwarn("Procurando area...;")
                    self.cmdMotores.roboAcionarMotores(25, -25)

        elif self.estadoResgatar == 1:
            if self.verificouArea: # area verifica true
                if dist < 8: # testar se eh so data msm, ja que o return do getDistancia ja eh um vetor indexado

                    if self.estadoArea == 1:
                        if not self.c.motorIsBusy():
                            self.cmdMotores.roboParar(2)
                            rospy.logwarn('Parei!')
                            self.estadoArea = 2
                        else:
                            rospy.logwarn('Esperando motores para poder parar')

                    elif self.estadoArea == 2:
                        if not self.c.motorIsBusy() and not self.c.garraIsBusy():
                            # self.cmdGarras.resgatar()
                            rospy.logwarn('Resgatei!')
                            self.estadoArea = 3
                            self.estadoRobo = self.RETORNAR()
                        else:
                            rospy.logwarn('Esperando motores/garrar para poder resgatar')

                else:
                    if self.estadoArea == 0: # inicio do resgate
                        if not self.c.motorIsBusy():
                            rospy.logwarn('Indo ate a area...')
                            self.cmdMotores.roboAcionarMotores(34,34)
                            self.estadoArea = 1
                        else:
                            rospy.logwarn('Esperando motores para poder ir para area')
                            
            else:
                if areaBool.existe.data and self.qntVisu > 10:
                    self.verificouArea = True
                elif areaBool.existe.data:
                    self.qntVisu = self.qntVisu + 1
                elif not areaBool.existe.data:
                    self.estadoPegar = 0 # deixou de verificar

    def pegar(self):
        
        coordenadas = self.c.getCoordenadaCirculo()

        if self.estadoPegar == 0:
            x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z
            
            raioPequeno = r < 54

            if self.encontrouBola and self.estadoPegar == 0:
                if not self.c.motorIsBusy() and not self.c.garraIsBusy():
                    self.cmdGarras.abrirMao()
                    self.cmdGarras.abaixarBraco()
                    self.encontrouBola = False # necessario?

            if not raioPequeno:
                rospy.logwarn("Estou longe")
                if not self.c.motorIsBusy():
                    self.cmdMotores.roboAcionarMotores(30, 32)
            else:
                self.estadoPegar = 1 # ta perto da vitima
        else:
            if self.estadoPegar == 1:
                if not self.c.motorIsBusy():
                    self.cmdMotores.roboParar(0.6)
                    rospy.logwarn("Parei;")
                    self.estadoPegar = 2

            elif self.estadoPegar == 2:
                # verificar o motor ajuda?
                # coloquei para impedir algum tipo de interferencia que possa acontecer
                if not self.c.motorIsBusy() and not self.c.garraIsBusy():
                    self.cmdGarras.fecharMao()
                    rospy.logwarn('Subi!')
                    self.estadoPegar = 3    

            elif self.estadoPegar == 3:
                if not self.c.garraIsBusy():
                    self.cmdGarras.subirBraco()
                    rospy.logwarn('Fechei!')
                    self.estadoPegar = 4

            elif self.estadoPegar == 4:
                if not self.c.motorIsBusy():
                    self.cmdMotores.roboParar(1)
                    rospy.logwarn('Peguei!')
                    self.estadoPegar = 5

            elif self.estadoPegar == 5: # aproveita loop callback para demorar um pouco para comecar
                self.estadoRobo = self.RESGATAR()

    def procurar(self):
        
        coordenadas = self.c.getCoordenadaCirculo()
        circle = self.c.getCirculo()
        # dist = ?

        rospy.logwarn("entrei aqui")

        if not self.encontrouBola:
            x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z

            if circle.existe.data:
                self.encontrouBola = True
                if not self.c.motorIsBusy(): # faz mesma coisa
                    self.cmdMotores.roboParar(1)
                    rospy.logwarn("Parei")
                    rospy.logwarn("Encontrei a vitima!")
                    self.encontrouBola = True
                    self.estadoRobo = self.PEGAR()
                    rospy.logwarn("Posicionado para pegar!")
            else:
                rospy.loginfo("Nao estou encontrando...")

                if not self.c.motorIsBusy():
                    self.cmdMotores.roboAcionarMotores(-30, 30)

        elif not self.c.motorIsBusy(): # faz mesma coisa
            self.cmdMotores.roboParar(1)
            rospy.logwarn("Parei")
            rospy.logwarn("Encontrei a vitima!")
            self.encontrouBola = True
            self.estadoRobo = self.PEGAR()
            rospy.logwarn("Posicionado para pegar!")

        # obs.: escolhi ser reduntante para que o robo pare depois
        # no caso dos motores ocupados

    def resetVars(self):
        self.estadoRobo = 0 # comeca procurando
        self.logIndex = 0

        self.encontrouBola = False
        self.estadoPegar = 0

        self.indexVolta = 0

        # resgate things 
        self.estadoResgatar = 0
        self.verificouArea = False
        self.estadoArea = 0
        self.qntVisu = 0        
    
    def main(self, msg):
        
        cliqBtn1 = self.c.getBtn(1).data
        cliqBtn3 = self.c.getBtn(3).data

        if cliqBtn1 and not self.pediuReset: # primeira execucao
            rospy.logwarn("Posso executar")
            self.podeExecutar = True
        elif cliqBtn3 and not self.pediuReset: # pede reset e para execucao
            rospy.logwarn("Parei porque pediram reset")
            self.pediuReset = True
            self.podeExecutar = False
        elif cliqBtn1 and self.pediuReset: # reseta execucao
            rospy.logwarn("Resetando execucao")
            self.podeExecutar = True # permite execucao inicial
            self.pediuReset = False
            self.resetVars()
        
        if self.podeExecutar:
            if self.estadoRobo == self.PROCURAR():
                if self.logIndex == 0:
                    self.logIndex = 1
                    rospy.logwarn("Estou procurando!")
        
                self.procurar()

            elif self.estadoRobo == self.PEGAR():
                if self.logIndex == 1:
                    self.logIndex = 2
                    rospy.logwarn("Vou pegar!")

                self.pegar()

            elif self.estadoRobo == self.RESGATAR():
                if self.logIndex == 2:
                    self.logIndex = 3
                    rospy.logwarn("Resgatando...")

                self.resgatar()
        
            elif self.estadoRobo == self.RETORNAR():
                if self.indexVolta == 0:
                    if not self.c.motorIsBusy():
                        self.cmdMotores.roboParaTras(1.6)
                        self.indexVolta = 1
                    else:
                        rospy.logwarn("Esperando motores para poder ir para tras")
                elif self.indexVolta == 1:
                    if not self.c.motorIsBusy():
                        self.cmdMotores.roboDir(.5)
                        self.indexVolta = 2
                    else:
                        rospy.logwarn("Esperando motores para poder ir para direita")
                elif self.indexVolta == 2:
                    if not self.c.motorIsBusy():
                        self.cmdMotores.roboParar(1)
                        self.resetVars()
                    else:
                        rospy.logwarn("Esperando motores para poder ir para direita")

if __name__ == "__main__":
    ros_node = TesteSala3()
    rospy.spin()