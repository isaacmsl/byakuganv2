#!/usr/bin/env python

import rospy
import message_filters
import cv2
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import Image
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolStamped, BotoesMsg
from cv_bridge import CvBridge

pubMotores = rospy.Publisher('ctrl_motores', Int32MultiArray, queue_size=10)
pubGarra = rospy.Publisher('ctrl_garras', Int32MultiArray, queue_size=10)
angAnt = 0
velAnt = 0
def map(x, in_min, in_max, out_min, out_max):
    if (x > in_max):
        x = in_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
def arduinoCamCb(refle, dist, circulo, botoes, coordenadas):
    global lock
    lock.acquire()
    maisEsq = refle.refletancia[0]
    esq = refle.refletancia[1]
    dir = refle.refletancia[2]
    maisDir = refle.refletancia[3]

    distFrontal =  dist.sensoresDistancia[0]
    distEsq = dist.sensoresDistancia[1]
    distDir = dist.sensoresDistancia[2]
    lock.release()

def get():
    global lock
    lock.acquire()
        #copia para variaveis locais
    lock.release()
    return


def lerSonar1():
    global lock
    lock.acquire()
    vSonar =  distFrontal
    lock.release()
    return vSonar

while(master.lerSonar1() > 10)

    if botoes.botao1.data:
        print 'botao 1 pressionado'
    if botoes.botao2.data:
        print 'botao 2 pressionado'
    if botoes.botao3.data:
        print 'botao 3 pressionado'

    #rospy.loginfo(coordenadas.vector)
    #rospy.loginfo(circulo.existe.data)
    if circulo.existe.data:
	if coordenadas.vector.x > 200:
		dataMotores.data = [25,-25]
	else:
		dataMotores.data = [-25, 25]
	ang = map(coordenadas.vector.x, 0, 400, 0, 179)
       	dataGarra.data = [ang, ang]
    else:
	#print 'else'
        dataMotores.data = [0,0]
        dataGarra.data = [0, 0]

    #rospy.loginfo(dataMotores.data)
    pubGarra.publish(dataGarra)
    pubMotores.publish(dataMotores)

def arduino_cam():
    rospy.init_node('arduino_cam', anonymous=True)
    subBotoes = message_filters.Subscriber('botoes', BotoesMsg)
    subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
    subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
    subCam = message_filters.Subscriber('tem_circulos', BoolStamped)
    subCoordenadas = message_filters.Subscriber('/coordenadas_circulos', Vector3Stamped)

    ts = message_filters.TimeSynchronizer([subRefle, subDistancia, subCam, subBotoes, subCoordenadas], 20)

    ts.registerCallback(arduinoCamCb)

    rospy.spin()
    #while
    #rospy.spinOnce()
    ##copia valores dos sensores
    ##estrategia
    ##copia valores para os atuadores

if __name__ == "__main__":
    try:
        ponte = CvBridge()
        dataGarra = Int32MultiArray()
        dataGarra.data = [0, 0]
        dataMotores = Int32MultiArray()
        dataMotores.data = [0, 0]
        arduino_cam()
    except rospy.ROSInterruptException:
        pass
