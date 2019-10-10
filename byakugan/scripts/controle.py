from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras
from geometry_msgs.msg import Vector3Stamped

class Controle:
    def __init__(self):
        self.__btns = BotoesMsg()
        self.__circulo = BoolStamped()
        self.__coordenadaCirculo = Vector3Stamped()
        self.__dist = SensoresDistanciaMsg()
        self.__centroid = BoolStamped()

    def btnsCb(self, btns):
        self.__btns = btns

    def temCirculoCb(self, circulo):
        self.__circulo = circulo

    def coordenadasCirculoCb(self, coordenadasCiruclo):
        self.__coordenadaCirculo = coordenadasCiruclo

    def distanciaCb(self, distancia):
        self.__dist = distancia
    
    def retanguloCb(self, centroid):
        self.__centroid = centroid
    
    def getDistancia(self, i):
        return self.__dist.sensoresDistancia[i]
        
