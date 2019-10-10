#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from std_msgs.msg import Int32MultiArray, Int8
from byakugan.msg import BoolGarras

class Garras():
    def __init__(self):
        rospy.Subscriber('cmdGarras', BoolGarras, self.__callback)

        # braco
        self.ANG_INICIAL_BAIXAR_BRACO = 130
        self.ANG_FINAL_BAIXAR_BRACO = 46

        self.ANG_INICIAL_SUBIR_BRACO = 46
        self.ANG_FINAL_SUBIR_BRACO = 130

        # mao
        self.ANG_INICIAL_ABRIR_MAO = 100
        self.ANG_FINAL_ABRIR_MAO = 46

        self.ANG_INICIAL_FECHAR_MAO = 46
        self.ANG_FINAL_FECHAR_MAO = 100

        self.DELAY = 0.005
        self.BRACO = 1 # diferenciando a publicacao para o braco e a mao
        self.MAO = 2 # diferenciando a publicacao para o braco e a mao

        self.cacheBraco = 2 # levantado
        self.cacheMao = 2 # fechada

        self.angAtualMao = 100
        self.angAtualBraco = 130

        self.dataStatus = Int8()

        # publisher
        self.rate = rospy.Rate(20)
        self.pubGarras = rospy.Publisher('ctrl_garras', Int32MultiArray, queue_size=10)
        self.pubStatus = rospy.Publisher("status_garras", Int8, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on ctrl_motores [std_msgs.msg/Int32MultiArray]")

    def __callback(self, dataGarras):
        # mao .. abrir = 1 / fechar = 2 / 0 = nothing
        # braco ..  abaixar = 1 / subir = 2 / 0 = nothing

        # testar

        dataMao = dataGarras.mao.data
        dataBraco = dataGarras.braco.data

        if dataMao == 1 and dataMao != self.cacheMao: # impede publicações desnecessárias
            self.__abrirMao()
            rospy.loginfo("Note: abrirMao")
            self.cacheMao = dataMao
            rospy.loginfo("Note: cacheMao was changed to " + str(dataMao))
        elif dataMao == 2 and dataMao != self.cacheMao:
            self.__fecharMao()
            rospy.loginfo("Note: fecharMao")
            self.cacheMao = dataMao
            rospy.loginfo("Note: cacheMao was changed to " + str(dataMao))
        elif dataMao > 2:
            self.__acionarMao(dataMao)

        if dataBraco == 2 and dataBraco != self.cacheBraco:
            self.__subirBraco()
            rospy.loginfo("Note: subirBraco")
            self.cacheBraco = dataBraco
            rospy.loginfo("Note: cacheBraco was changed to " + str(dataBraco))
        elif dataBraco == 1 and dataBraco != self.cacheBraco:
            self.__abaixarBraco()
            rospy.loginfo("Note: abaixarBraco")
            self.cacheBraco = dataBraco
            rospy.loginfo("Note: cacheBraco was changed to " + str(dataBraco))
        elif dataBraco > 2:
            self.__acionarBraco(dataBraco)

    def __setPosicao(self, servo, angInicial, angFinal, delay=None):
        if delay is None:
            delay = self.DELAY

        dataGarras = Int32MultiArray()

        diferencaAngs = abs(angFinal - angInicial)

        if diferencaAngs % 2 != 0:
            diferencaAngs += 1
        
        passosAngulo = int(diferencaAngs/4) # vai definir 4 angulos para a movimentacao

        # diz que para o no de controle que a garra esta ocupada
        self.dataStatus.data = 1
        self.pubStatus.publish(self.dataStatus)

        if angInicial > angFinal: # diminuir angulo
            # publica em espaços aos poucos do angInicial ao angFinal
            passosAngulo = passosAngulo * -1 # para decrementar
            for i in range(angInicial, angFinal, passosAngulo):
                if servo == self.BRACO: # diferenciando a publicacao para o braco e a mao
                    dataGarras.data = [self.angAtualMao, i] # [braco, mao]
                    self.angAtualBraco = i
                elif servo == self.MAO:
                    dataGarras.data = [i, self.angAtualBraco] # [braco, mao
                    self.angAtualMao = i

                self.pubGarras.publish(dataGarras)
                rospy.loginfo("[PUBLISHED] ctrl_garras -> " + str(dataGarras.data))
                #print dataGarras
                if not i == angFinal:
                    time.sleep(float(delay))

        else:
            # publica em espaços aos poucos do angInicial ao angFinal
            for i in range(angInicial, angFinal, passosAngulo):
                if servo == self.BRACO: # diferenciando a publicacao para o braco e a mao
                    dataGarras.data = [self.angAtualMao, i] # [braco, mao]
                    self.angAtualBraco = i
                elif servo == self.MAO:
                    dataGarras.data = [i, self.angAtualBraco] # [braco, mao
                    self.angAtualMao = i

                self.pubGarras.publish(dataGarras)
                rospy.loginfo("[PUBLISHED] ctrl_garras -> " + str(dataGarras.data))
                #print dataGarras
                if not i == angFinal:
                    time.sleep(float(delay))
        
        # diz que para o no de controle que a garra esta ocupada
        self.dataStatus.data = 0
        self.pubStatus.publish(self.dataStatus)

    def __acionarMao(self, mao):
        self.__setPosicao(self.MAO, self.angAtualMao, mao)
    def __acionarBraco(self, braco):
        self.__setPosicao(self.BRACO, self.angAtualBraco, braco)
    def __abaixarBraco(self):
        self.__setPosicao(self.BRACO, self.ANG_INICIAL_BAIXAR_BRACO, self.ANG_FINAL_BAIXAR_BRACO)
    def __subirBraco(self):
        self.__setPosicao(self.BRACO, self.ANG_INICIAL_SUBIR_BRACO, self.ANG_FINAL_SUBIR_BRACO)
    def __abrirMao(self):
        self.__setPosicao(self.MAO, self.ANG_INICIAL_ABRIR_MAO, self.ANG_FINAL_ABRIR_MAO)
    def __fecharMao(self):
        self.__setPosicao(self.MAO, self.ANG_INICIAL_FECHAR_MAO, self.ANG_FINAL_FECHAR_MAO)

if __name__ == "__main__":
    rospy.init_node('garras', anonymous=False)
    garras = Garras()
    rospy.spin()
