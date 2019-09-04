#!/usr/bin/env python
import rospy 
import threading
import cmdMotores
from feedCamera import FeedCamera
from byakugan.msg import CtrlMotores

class ProcuraVitima:
    def __init__(self):
        rospy.init_node("ProcuraVitima", anonymous=False)
        self.fc = FeedCamera()
        self.pubMotores = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10)
        self.cmd = cmdMotores.CmdMotores(self.pubMotores)
        
    def loop(self):   
        while not self.fc.getVitima():
            self.cmd.roboAcionarMotores(-30, 30)
        self.cmd.roboAcionarMotores(0,0)

if __name__ == "__main__":
    try:
        pv = ProcuraVitima()
        pv.fc.register()
        threading.Thread(target=pv.loop()).start() 
        rospy.spin()
    except rospy.ROSInterruptException:
        pass