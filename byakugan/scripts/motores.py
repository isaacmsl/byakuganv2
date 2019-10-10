#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray, Int8
from byakugan.msg import CtrlMotores
import time

class Motores():
    def __init__(self):

        self.VEL_DIR_FRENTE_RAMPA = 88
        self.VEL_DIR_TRAS_RAMPA = 68

        self.VEL_ESQ_FRENTE_RAMPA = 85
        self.VEL_ESQ_TRAS_RAMPA = 65

        self.VEL_DIR_FRENTE = 48
        self.VEL_DIR_TRAS = -48

        self.VEL_ESQ_FRENTE = 45
        self.VEL_ESQ_TRAS = -45

        self.dataMotores = Int32MultiArray()
        self.dataStatus = Int8()

        # publisher
        rospy.init_node("motores", anonymous=False)

        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        self.pubStatus = rospy.Publisher("status_motores", Int8, queue_size=10, latch=True)
        
        rospy.loginfo("Setup publisher on ctrl_motores [std_msgs.msg/Int32MultiArray]")
        rospy.Subscriber("cmdMotores", CtrlMotores, self.callback)
        rospy.loginfo("Setup subscriber on cmdMotores [byakugan_msgs.msg/CtrlMotores]")

    def callback(self, dataMotores):

        velEsq = dataMotores.esq.data
        velDir = dataMotores.dir.data
        esqFrente = (velEsq == 1)
        dirFrente = (velDir == 1)

        vel_default = (velEsq < 2 and velDir < 2) # else - acionarMotores(varEsq, varDir)

        delayPub = dataMotores.delay.data

        if vel_default:
            if not dataMotores.rampa.data:
                if esqFrente and dirFrente:
                    self.__roboEmFrente(delayPub)
                elif dirFrente:
                    self.__roboEsq(delayPub)
                elif esqFrente:
                    self.__roboDir(delayPub)
                elif velEsq < 0 and velDir < 0:
                    self.__roboParaTras(delayPub)
                else:
                    self.__roboParar(delayPub)
        else:
            self.__roboAcionarMotores(velEsq, velDir, delayPub)
        '''
        elif esqFrente and dirFrente:
            self.emFrenteRampa(delayPub)
        elif dirFrente:
            self.esquerdaRampa(delayPub)
        elif esqFrente:
            self.direitaRampa(delayPub)
        '''

    def __pubDelayMotores(self, velEsq, velDir, delay):
        dataMotores = Int32MultiArray()
        tInicio = time.time()
        tAtual = tInicio

        iAnterior = -1

        dataMotores.data = [velEsq, velDir]

        # diz que para o no de controle que o motores esta ocupado
        self.dataStatus.data = 1
        self.pubStatus.publish(self.dataStatus)

        # publica pela primeira vez
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] - " + str(dataMotores.data))

        # publicando com delay
        while tAtual - tInicio < delay: # pula se delay for zero
            iAtual = int(tAtual - tInicio)
            if iAnterior != iAtual:
                rospy.loginfo("[LOOPING...] - " + str(iAtual)) # informa laco delay
                iAnterior = iAtual
            tAtual = time.time()

        if delay != 0: # quando houver comando motores com delay
            dataMotores.data = [0, 0]
            self.pubMotores.publish(dataMotores)
            rospy.loginfo("[STOPPING] - " + str(dataMotores.data))
        
        # diz que para o no de controle que o motores esta livre
        self.dataStatus.data = 0
        self.pubStatus.publish(self.dataStatus)

    # seguir linha
    def __roboAcionarMotores(self, esq, dir, delay=0):
        self.__pubDelayMotores(esq, dir, delay)

    def __roboEmFrente(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_FRENTE, self.VEL_DIR_FRENTE, delay)
    def __roboDir(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_FRENTE, self.VEL_DIR_TRAS, delay)
    def __roboEsq(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_TRAS, self.VEL_DIR_FRENTE, delay)
    def __roboParaTras(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_TRAS, self.VEL_DIR_TRAS, delay)
    def __roboParar(self, delay=0):
        self.__pubDelayMotores(0, 0, delay)

    '''
    # subir rampa
    def roboEmFrenteRampa(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_FRENTE_RAMPA, delay)
    def roboDirRampa(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_TRAS_RAMPA, delay)
    def roboEsqRampa(self, delay=0):
        self.__pubDelayMotores(self.VEL_ESQ_TRAS_RAMPA, self.VEL_DIR_FRENTE_RAMPA, delay)
    '''

if __name__ == "__main__":
    motores = Motores()
    rospy.spin()
