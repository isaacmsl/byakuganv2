#!/usr/bin/env python

import rospy
from byakugan.msg import BoolGarras
import time

class CmdGarras:
    def __init__(self, pub):
        self.pub = pub
        self.dataGarras = BoolGarras()

    def resgatar(self):
        self.dataGarras.mao.data = 0
        self.dataGarras.braco.data = 80
        self.pub.publish(self.dataGarras)
        self.abrirMao()
        for i in range (0, 2):
            self.dataGarras.braco.data = 100
            self.pub.publish(self.dataGarras)
            self.dataGarras.braco.data = 115
            self.pub.publish(self.dataGarras)

        self.fecharMao()
        self.dataGarras.braco.data = 130
        self.pub.publish(self.dataGarras)

    def abrirMao(self):
        self.dataGarras.mao.data = 1
        self.dataGarras.braco.data = 0
        self.pub.publish(self.dataGarras)
    def fecharMao(self):
        self.dataGarras.mao.data = 2
        self.dataGarras.braco.data = 0
        self.pub.publish(self.dataGarras)
    def subirBraco(self):
        self.dataGarras.braco.data = 2
        self.dataGarras.mao.data = 0
        self.pub.publish(self.dataGarras)
    def abaixarBraco(self):
        self.dataGarras.braco.data = 1
        self.dataGarras.mao.data = 0
        self.pub.publish(self.dataGarras)
