#!/usr/bin/env python

import rospy
import threading
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BotoesMsg

class Sensores:
    '''
    ___refletancia
    ___distancia
    ___botoes
    ___lock
    '''
    def __init__(self):
        self.__lock = threading.Lock()

        self.__lock.acquire()
        try:
            self.__refletancia = RefletanciaMsg()
            self.__distancia = SensoresDistanciaMsg()
            self.__botoes = BotoesMsg()
        finally:
            self.__lock.release()

    def setValues(self, refle, dist, btns):
        self.__lock.acquire()
        try:
            self.__refletancia = refle
            self.__distancia = dist
            self.__botoes = btns
        finally:
            self.__lock.release()

    def getRefle(self, n):
        self.__lock.acquire() #pega o lock
        try:
            return self.__refletancia.refletancia[n] #le a variavel
        finally:
            self.__lock.release() #solta o lock

    def getDist(self, n):
        self.__lock.acquire() #pega o lock
        try:
            return self.__distancia.sensoresDistancia[n] #le a variavel
        finally:
            self.__lock.release() #solta o lock


    def getBtn1(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao1.data
        finally:
            self.__lock.release()

    def getBtn2(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao2.data
        finally:
            self.__lock.release()

    def getBtn3(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao3.data
        finally:
            self.__lock.release()
