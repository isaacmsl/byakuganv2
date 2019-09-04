#!/usr/bin/env python

import rospy
from SensorsListener import SensorsListener
#import motores

class Refletancia():
    def __init__(self, sl):
        self.sl = sl

    def maisEsqBranco(self): return self.sl.getRefle(0) > 4
    def esqBranco(self): return self.sl.getRefle(1) > 4
    def dirBranco(self): return self.sl.getRefle(2) > 4
    def maisDirBranco(self): return self.sl.getRefle(3) > 4

    def b_b_b_b(self):
        return self.maisEsqBranco() and self.esqBranco() and self.dirBranco() and self.maisDirBranco()

    def p_p_p_p(self):
        return not self.maisEsqBranco() and not self.esqBranco() and not self.dirBranco() and not self.maisDirBranco()

    def p_b_b_b(self):
        return not maisEsqBranco() and self.esqBranco() and self.dirBranco() and self.maisDirBranco()

    def p_p_b_b(self):
        return not self.maisEsqBranco() and not self.esqBranco() and self.dirBranco() and self.maisDirBranco()

    def p_p_p_b(self):
        return not self.maisEsqBranco() and not self.esqBranco() and not self.dirBranco() and self.maisDirBranco()

    def b_p_p_p(self):
        return self.maisEsqBranco() and not self.esqBranco() and not self.dirBranco() and not self.maisDirBranco()

    def b_b_p_p(self):
        return self.maisEsqBranco() and self.esqBranco() and not self.dirBranco() and not self.maisDirBranco()

    def b_b_b_p(self):
        return self.maisEsqBranco() and self.esqBranco() and self.dirBranco() and not self.maisDirBranco()

    def p_b_p_b(self):
        return not self.maisEsqBranco() and self.esqBranco() and not self.dirBranco() and self.maisDirBranco()

    def p_b_b_p(self):
        return not self.maisEsqBranco() and self.esqBranco() and self.dirBranco() and not self.maisDirBranco()

    def b_p_b_p(self):
        return self.maisEsqBranco() and not self.esqBranco() and self.dirBranco() and not self.maisDirBranco()

    def b_p_p_b(self):
        return self.maisEsqBranco() and not self.esqBranco() and not self.dirBranco() and self.maisDirBranco()

    def p_b_p_p(self):
        return not self.maisEsqBranco() and self.esqBranco() and not self.dirBranco() and not self.maisDirBranco()

    def p_p_b_p(self):
        return not self.maisEsqBranco() and not self.esqBranco() and self.dirBranco() and not self.maisDirBranco()

    def b_p_b_b(self):
        return self.maisEsqBranco() and not self.esqBranco() and self.dirBranco() and self.maisDirBranco()

    def b_b_p_b(self):
        return self.maisEsqBranco() and self.esqBranco() and not self.dirBranco() and self.maisDirBranco()

'''
Utilizar com a classe feita de testeEstrategia
if __name__ == "__main__":
    try:

        sl = SensorsListener()
        threading.Thread(target=showValue).start()
        sl.register()
'''
