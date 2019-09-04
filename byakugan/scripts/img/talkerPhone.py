#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import requests
import numpy as np 

url = "http://10.0.0.109:8080/shot.jpg"

def talker():

	pub = rospy.Publisher('topico_img', Image, queue_size=10)
	rospy.init_node('talkerPhone', anonymous=False)
	rate = rospy.Rate(30) # 30hz

	bridge = CvBridge()

	while not rospy.is_shutdown():
		
		img_resp = requests.get(url)
		img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
		frame = cv2.imdecode(img_arr, -1)

		frame = cv2.resize(frame, (400, 400))

		frame = cv2.flip(frame, 180)

		cv2.imshow('imagemPhone', frame)

		pub.publish(bridge.cv2_to_imgmsg(frame))
		rate.sleep()

		cv2.waitKey(1)

	cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
