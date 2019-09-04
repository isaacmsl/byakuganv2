#!/usr/bin/env python

import rospy
import os
import cmdGarras
import message_filters
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import SensoresDistanciaMsg, BoolGarras, CtrlMotores, BoolStamped
from std_msgs.msg import Int32MultiArray
import cmdMotores
import time

class PegarBola:
    def callback(self, init, coordenadas):
        if init.existe.data and not self.executou:
            x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z

            if(r < 48 and self.encontrei == False ):
                rospy.loginfo("Estou longe")
                self.cmdMotores.roboAcionarMotores(30, 34)
            else:
                self.cmdMotores.roboAcionarMotores(0,0)
                rospy.loginfo("Estou perto")
                self.encontrei = True

                self.cmdGarras.abrirMao()
                self.cmdGarras.abaixarBraco()
                self.cmdGarras.fecharMao()
                self.cmdGarras.subirBraco()
                time.sleep(2)
                self.executou = True
        else:
            self.initResgatar()

    def initResgatar(self):
        initData = BoolStamped()
        initData.existe.data = True
        self.pubResgatar.publish(initData)
        self.executou = True

    def __init__(self):
        rospy.init_node("pegarVitima", anonymous=False)

        self.encontrei = False

        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.pubResgatar = rospy.Publisher("initResgatar", BoolStamped, queue_size=10, latch=True)

        self.cmdGarras = cmdGarras.CmdGarras(self.pubGarras)


        self.pubMotores = rospy.Publisher('cmdMotores', CtrlMotores , queue_size=10, latch=True)
        self.cmdMotores = cmdMotores.CmdMotores(self.pubMotores)
        self.executou = False

        subInit = message_filters.Subscriber('initPegar', BoolStamped)
        subCoordenadas = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        ts = message_filters.TimeSynchronizer([subInit, subCoordenadas], 20)
        ts.registerCallback(self.callback)


if __name__ == "__main__":
    pegaBola = PegarBola()
    rospy.spin()
