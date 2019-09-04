#!/usr/bin/env python

import rospy
import curses
import os
from cmdGarras import CmdGarras
from cmdMotores import CmdMotores
from byakugan.msg import CtrlMotores, BoolGarras

class Teleop:
   def __init__(self):
      rospy.init_node("teleop", anonymous=True)
      self.pubMotores = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10)
      self.pubGarras = rospy.Publisher("cmdGarras", BoolGarras, queue_size=10)
      self.cmdGarras = CmdGarras(self.pubGarras)
      self.cmdMotores = CmdMotores(self.pubMotores)
      self.running = 0
      curses.wrapper(self.main)

   def main(self, win):
      win.nodelay(True)
      key=""
      win.clear()
      win.addstr("Detected key:")
      while 1:
         try:
            key = win.getkey()
            win.clear()
            win.addstr("Detected key:")

            if(key == 'KEY_UP'):
               win.addstr("frente")
               if self.running == 0:
                  self.cmdMotores.roboEmFrente()
                  self.running = 1
               else:
                  self.running = 0
                  self.cmdMotores.roboParar()
            elif(key == 'KEY_DOWN'):
               win.addstr("baixo")
               if self.running == 0:
                  self.cmdMotores.roboParaTras()
                  self.running = 1
               else:
                  self.running = 0
                  self.cmdMotores.roboParar()
            elif(key == 'KEY_LEFT'):
               win.addstr("esquerda")
               if self.running == 0:
                  self.cmdMotores.roboEsq()
                  self.running = 1
               else:
                  self.running = 0
                  self.cmdMotores.roboParar()
            elif(key == 'KEY_RIGHT'):
               win.addstr("direita")
               if self.running == 0:
                  self.cmdMotores.roboDir()
                  self.running = 1
               else:
                  self.running = 0
                  self.cmdMotores.roboParar()
            elif(key == 'q'):
               win.addstr("abaixa")
               self.cmdGarras.abrirMao()
               self.cmdGarras.abaixarBraco()
            elif(key == 'r'):
               win.addstr("levanta")
               self.cmdGarras.fecharMao()
               self.cmdGarras.subirBraco()
            elif(key == 's'):
               win.addstr("salvar")
               self.cmdGarras.resgatar()

            if key == os.linesep:
               break
         except Exception as e:
            # No input
            pass

if __name__ == "__main__":
   t = Teleop()
   rospy.spin()
