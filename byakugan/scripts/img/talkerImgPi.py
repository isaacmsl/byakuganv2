#!/usr/bin/env python

import rospy
import cv2
import time
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

def talkerImg(compImg):
	ponte = CvBridge()
	np_arr = np.fromstring(compImg.data, np.uint8)
	imgCV = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

  	imgCV = cv2.flip(imgCV, 2)
	imgMsg = ponte.cv2_to_imgmsg(imgCV, "bgr8")

	pub.publish(imgMsg)
	pub2.publish(compImg)

	#?rate.sleep()

if __name__ == "__main__":
	try:
		rospy.init_node('talkerImgPi', anonymous=True)
		pub = rospy.Publisher('topico_img', Image, queue_size=10)
		pub2 = rospy.Publisher('compressed_img', CompressedImage, queue_size=10)
		rate = rospy.Rate(20)
		rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, talkerImg)
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
