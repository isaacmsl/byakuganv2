#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray
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

        # publisher
        rospy.init_node("motores", anonymous=False)

        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        rospy.loginfo("Setup publisher on ctrl_motores [std_msgs.msg/Int32MultiArray]")
        rospy.Subscriber("cmdMotores", CtrlMotores, self.callback)
        rospy.loginfo("Setup subscriber on cmdMotores [byakugan_msgs.msg/CtrlMotores]")

    def callback(self, dataMotores):

        rospy.loginfo(rospy.get_caller_id() + " - msg received!")

        esq = dataMotores.esq.data
        dir = dataMotores.dir.data
        esqFrente = (esq == 1)
        dirFrente = (dir == 1)

        vel_default = (esq < 2 and dir < 2) # else - acionarMotores(varEsq, varDir)

        delayPub = dataMotores.delay.data

        if vel_default:
            if not dataMotores.rampa.data:
                if esqFrente and dirFrente:
                    self.__roboEmFrente(delayPub)
                elif dirFrente:
                    self.__roboEsq(delayPub)
                elif esqFrente:
                    self.__roboDir(delayPub)
                elif esq < 0 and dir < 0:
                    self.__roboParaTras(delayPub)
                else:
                    self.__roboParar(delayPub)
        else:
            self.__roboAcionarMotores(esq, dir, delayPub)
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
        if delay == 0:
                self.pubMotores.publish(dataMotores)
                rospy.loginfo("[PUBLISHED] - " + str(dataMotores.data))

        while tAtual - tInicio < delay: #
            iAtual = int(tAtual - tInicio)
            if iAnterior != iAtual:
                iAnterior = iAtual
                self.pubMotores.publish(dataMotores)
                rospy.loginfo("[PUBLISHED] - " + str(dataMotores.data))
                rospy.loginfo("[PUBLISHING...] time:" + str(iAtual))
            tAtual = time.time()

        if delay != 0:
            dataMotores.data = [0, 0]
            self.pubMotores.publish(dataMotores)
            rospy.loginfo("[PUBLISHED] - " + str(dataMotores.data))

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
