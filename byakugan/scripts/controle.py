from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores, BoolGarras
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int8

class Controle:
    def __init__(self):
        self.__btns = BotoesMsg()
        self.__circulo = BoolStamped()
        self.__coordenadaCirculo = Vector3Stamped()
        self.__dist = SensoresDistanciaMsg()
        self.__centroid = BoolStamped()
        self.__statusMotores = Int8()
        self.__statusGarras = Int8()

    def btnsCb(self, btns): self.__btns = btns
    def getBtn(self, i):
        if i == 1:
            return self.__btns.botao1
        if i == 2:
            return self.__btns.botao2
        if i == 3:
            return self.__btns.botao3
            
    
    def temCirculoCb(self, circulo): self.__circulo = circulo
    def getCirculo(self): return self.__circulo

    def coordenadasCirculoCb(self, coordenadasCiruclo): self.__coordenadaCirculo = coordenadasCiruclo
    def getCoordenadaCirculo(self): return self.__coordenadaCirculo
    
    def distanciaCb(self, distancia): self.__dist = distancia
    def getDistancia(self, i): return self.__dist.sensoresDistancia[i]

    def retanguloCb(self, centroid): self.__centroid = centroid
    def getCentroid(self): return self.__centroid
    
    def statusMotores(self, statusMotores): self.__statusMotores = statusMotores
    def motorIsBusy(self): return self.__statusMotores.data

    def statusGarras(self, statusGarras): self.__statusGarras = statusGarras
    def garraIsBusy(self): return self.__statusGarras.data

    
    
    
        
        
