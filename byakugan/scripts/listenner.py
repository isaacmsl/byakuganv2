#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Int8
from cv_bridge import CvBridge, CvBridgeError # usado para conversao data img

arqCasc = '/home/paulo/Opencv/haarcascade/closed_frontal_palm.xml'

# resolucao
width = 400
height = 400

handCascade = cv2.CascadeClassifier(arqCasc)

detectedAlready = False
    
def callback(data):

	bridge = CvBridge()

	imagem = bridge.imgmsg_to_cv2(data) # conversao de data img

	hands = handCascade.detectMultiScale(
	imagem,
		minNeighbors= 30,
		minSize=(30, 30),
		maxSize=(200,200)
	)

	# usado para publicar somento quando houver deteccao
	hasDetected = False

	# usados na hora de publicacao
	centroReal = 0
	centroReduzido = 0 # publica entre 0 e 127 (int8)

	# Desenha um retangulo nas deteccoes
	for (x, y, w, h) in hands:

		hasDetected = True

		centroReal = x + (w/2)
		centroReduzido = (127 * centroReal)/400

		cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 5)
		cv2.putText(imagem, "",(x - 100, y), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0))

	if (hasDetected):
		'''
		infoPub = (centroReal, centroReduzido)

		print("Real/Pub: ", infoPub)

		pub.publish(centroReduzido) # so publica valor reduzido
		'''
		infoPub = (centroReal, centroReduzido)
		
		if (centroReal < width/2):

			print("Real/Pub (ESQ): ", infoPub)

			pub.publish(centroReduzido)
		else:

			print("Real/Pub (DIR): ", infoPub)

			pub.publish(centroReduzido)


	cv2.imshow('imagemLida', imagem)

	cv2.waitKey(1)

def listenner():

	global pub

	rospy.init_node('listennerTalkerCoor', anonymous=False)
	pub = rospy.Publisher('rosserial/coordenadas', Int8, queue_size=10)
	rospy.Subscriber('topico_img', Image, callback)

	rospy.spin()


if __name__ == "__main__":
	try:
		listenner()
	except rospy.ROSInterruptException:
		pass
