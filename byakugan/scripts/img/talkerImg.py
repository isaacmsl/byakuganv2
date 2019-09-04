#!/usr/bin/env python
import rospy 
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class TalkerImg:
	def __init__(self):
		rospy.init_node("talkerCamImg", anonymous=False)
		rospy.loginfo("Starting node " + rospy.get_name())

		self.camera = cv2.VideoCapture(1)
		
		while not rospy.is_shutdown():
			_, frame = self.camera.read()
			frame = cv2.resize(frame, (320,240))

			cv2.namedWindow('IMG', cv2.WINDOW_NORMAL)
			cv2.imshow('IMG', frame)

			if cv2.waitKey(1) == ord('s'):
				break
		

if __name__ == "__main__":
	ros_node = TalkerImg()