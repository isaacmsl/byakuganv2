#!/usr/bin/env python
import rospy
import cmdMotores
from controle import Controle
from std_msgs.msg import Empty, Int8
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras
from geometry_msgs.msg import Vector3Stamped

class TesteSala3:
    def __init__(self):
        rospy.init_node("sala3", anonymous=True)

        self.c = Controle()

        self.pubMotores = rospy.Publisher('cmdMotores', CtrlMotores , queue_size=10, latch=True)
        self.cmdMotores = cmdMotores.CmdMotores(self.pubMotores)

        rospy.Subscriber("ctrl", Empty, self.main)

        rospy.Subscriber('botoes_init', BotoesMsg, self.c.btnsCb)
        rospy.Subscriber("tem_circulos", BoolStamped, self.c.temCirculoCb)
        rospy.Subscriber("coordenadas_circulos", Vector3Stamped, self.c.coordenadasCirculoCb)
        rospy.Subscriber("distancia", SensoresDistanciaMsg, self.c.distanciaCb)
        rospy.Subscriber("centroid_rectangle", BoolStamped, self.c.retanguloCb)
        rospy.Subscriber("status_motores", Int8, self.c.statusMotores)
        rospy.Subscriber("status_garras", Int8, self.c.statusGarras)
    
    def PROCURAR(self): return 0
    '''
    def PEGAR(self): return 1
    def RESGATAR(self): return 2
    def RETORNAR(self): return 3
    '''
    def main(self, msg):
        if not self.c.motorIsBusy():
            rospy.loginfo("Publiquei")
        else:
            rospy.loginfo("Esperando")

        

if __name__ == "__main__":
    ros_node = TesteSala3()
    rospy.spin()