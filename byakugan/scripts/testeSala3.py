#!/usr/bin/env python
import rospy 
from controle import Controle
from std_msgs.msg import Empty
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras
from geometry_msgs.msg import Vector3Stamped

class TesteSala3:
    def __init__(self):
        rospy.init_node("sala3", anonymous=True)

        self.c = Controle()

        rospy.Subscriber("ctrl", Empty, self.controlCb)

        rospy.Subscriber('botoes_init', BotoesMsg, self.c.btnsCb)
        rospy.Subscriber("tem_circulos", BoolStamped, self.c.temCirculoCb)
        rospy.Subscriber("coordenadas_circulos", Vector3Stamped, self.c.coordenadasCirculoCb)
        rospy.Subscriber("distancia", SensoresDistanciaMsg, self.c.distanciaCb)
        rospy.Subscriber("centroid_rectangle", BoolStamped, self.c.retanguloCb)
    
    
    def controlCb(self, msg):
        rospy.loginfo(self.c.getDistancia(0))        
        

if __name__ == "__main__":
    ros_node = TesteSala3()
    rospy.spin()