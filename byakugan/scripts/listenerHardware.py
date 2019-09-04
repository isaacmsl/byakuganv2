#!/usr/bin/env python

import rospy
import cv2
import message_filters
from std_msgs.msg import Float64MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, LedMsg, BotoesMsg

leds = LedMsg()
pubLeds = rospy.Publisher('ctrl_leds', LedMsg, queue_size=10)
def callbackHardware(refle, dist, btns):
    '''
    rospy.loginfo('refletancia ' + str(refle.refletancia))
    rospy.loginfo('distancia ' + str(dist.sensoresDistancia))
    '''

    leds.led1.data = False
    leds.led2.data = False
    leds.led3.data = False 

    if(btns.botao1.data): leds.led1.data = True
    if(btns.botao2.data): leds.led2.data = True
    if(btns.botao3.data): leds.led3.data = True
    
    pubLeds.publish(leds)
    
def listenerHardware():
    rospy.init_node('listenerHardware', anonymous=True)
    
    subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
    subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
    subBtns = message_filters.Subscriber('botoes', BotoesMsg)

    ts = message_filters.TimeSynchronizer([subRefle, subDistancia, subBtns], 10)
    ts.registerCallback(callbackHardware)

    rospy.spin()

if __name__ == "__main__":
	try:
		listenerHardware()
	except rospy.ROSInterruptException:
		pass
