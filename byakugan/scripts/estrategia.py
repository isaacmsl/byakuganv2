#!/usr/bin/env python

import rospy
import threading
from std_msgs.msg import Int32MultiArray
from SensorsListener import SensorsListener
#import motores

class Estrategia():
    def __init__(self):

        self.rospy.init_node('estrategia', anonymous=False)

        self.publisher = EstPublisher()

        self.posicaoRobo = 1 # 1 == SALA 1 E 2 // 2 == RAMPA // 3 == SALA

        # sensores
        self.sl = SensorsListener()
        self.refle = Refletancia(self.sl)
        #self.btns = Botoes()
        #self.sonares = Sonares()

    '''
    def acionarMotores(esq, dir):
        dataMotores.data = [esq, dir]
        pubMotores.publish(dataMotores)
        rate.sleep()
    '''

    def loop():

        if self.posicaoRobo == 1:
            if refle.b_b_b_b():
                self.publisher.roboEmFrente()
            elif refle.b_p_b_b():
                self.publisher.roboEsq()
            elif refle.b_b_p_b():
                self.publisher.roboDir()
            elif p_p_b_b() or p_p_p_b():
                while not esqBranco():
                    self.publisher.roboEmFrente()
                while esqBranco():
                    self.publisher.roboEsq()
                while not esqBranco():
                    self.publisher.roboEsq()
                while not dirBranco():
                    self.publisher.roboDir()
            elif b_b_p_p() or b_p_p_p():
                while not dirBranco():
                    self.publisher.roboEmFrente()
                while dirBranco():
                    self.publisher.roboDir()
                while not dirBranco():
                    self.publisher.roboDir()
                while not esqBranco():
                    self.publisher.roboEsq()

            rate.sleep() # ?

if __name__ == "__main__":
    try:
        est = Estrategia()
        threading.Thread(target=est.loop()).start() # ?
        est.sl.register()
    except rospy.ROSInterruptException:
        pass
