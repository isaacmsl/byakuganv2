#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import os
from sensor_msgs.msg import CompressedImage
from byakugan.msg import BoolStamped

class FindRectangle:
    def __init__(self):
        rospy.init_node('findRectangle', anonymous=False)

        self.pub = rospy.Publisher('centroid_rectangle', BoolStamped, queue_size=10, latch=True)
        rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, self.callback)

        self.img = None
        self.thresh = None
        self.CENTER_X = int((320/2))

    def isBigDist(self, approx):
        approxRavel = approx.ravel() # transforma em um vetor
        points = []
        pointsX = []
        pointsY = []
        for i in range(0, len(approxRavel) - 1, 2): # vai adicionando os pontos do contorno
            x  = approxRavel[i]
            y  = approxRavel[i + 1]
            pointsX.append(x) # vai ser usado para saber o comprimento dos pontos
            pointsY.append(y) # vai ser usado para saber o altura dos pontos
            points.append((x,y)) # pontos do objeto

        xInicial = min(pointsX)
        xFinal = max(pointsX)
        yInicial = min(pointsY)
        yFinal = max(pointsY)

        compX = abs(xFinal - xInicial)
        compY = abs(yFinal - yInicial)

        diferenca = abs(compX - compY)

        #print compX, compY
        #print diferenca

        if compY < 30:
            return False

        return diferenca > 100 # if true eh retangulo else bola preta

    def getArea(self, cnt): return cv2.contourArea(cnt)

    def getCentroid(self, cnt, imgCV):
        M = cv2.moments(cnt)
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY

    def drawRectangle(self, cnt, width):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(self.img,[box],0,(0,255, 0), width)

    def cookImg(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5) # interfere?
        gray = 255 - gray

        _, self.thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        _, contours, _= cv2.findContours(self.thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def find(self):
        try:
            contours = self.cookImg()
            self.drawRectangle(contours[len(contours) - 1], 10) # draw contorno da propria img
            contours = self.cookImg() # cozinha a img novamente separando possiveis contours colados na img inicial

            indexCntImg = len(contours) - 1

            if indexCntImg == 0:
                areaBool = BoolStamped()
                areaBool.existe.data = False
                self.pub.publish(areaBool)

            for i in range(0, indexCntImg): # -1 impede de draw contour da propria img

                cnt = contours[i]

                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)

                cX, cY = self.getCentroid(cnt, self.img) # pega centro do contorno
                #print cX, cY

                area = self.getArea(cnt)

                # aproxima pontos do contorno - corners
                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
                #print approx.ravel()

                if self.isBigDist(approx): # verifica se o contorno eh retangulo
                    # draw centro do contorno e retangulo no contorno
                    print area

                    areaBool = BoolStamped()
                    areaBool.existe.data = True

                    if area > 20000.0:
                        areaBool.centroid.data = 111 # robo muito proximo a area
                    else:
                        areaBool.centroid.data = int(cX - self.CENTER_X)
                    self.pub.publish(areaBool)
                else:
                    areaBool = BoolStamped()
                    areaBool.existe.data = False
                    self.pub.publish(areaBool)

        except: # ???
            rospy.loginfo('error in img')

    def callback(self, compressedImg):
        np_arr = np.fromstring(compressedImg.data, np.uint8)
    	self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    	self.img = cv2.flip(self.img, 2)
        self.find()

if __name__ == "__main__":
    fr = FindRectangle()
    rospy.spin()
