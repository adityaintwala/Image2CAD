# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
from Core.Math.Point2 import Point2

class Eraser():

    @staticmethod
    def ErasePixel(img, pixel):
        img.itemset((pixel[0], pixel[1], 0), 255)
        img.itemset((pixel[0], pixel[1], 1), 255)
        img.itemset((pixel[0], pixel[1], 2), 255)
        return img

    @staticmethod
    def EraseLine(img, p1, p2):
         P1 = (int(p1.x), int(p1.y))
         P2 = (int(p2.x), int(p2.y))
         Eraser.checkForVicinity(img,p1,p2)
         cv2.line(img, P1, P2, (255,255,255),5)
         return img

    @staticmethod
    def checkForVicinity(img, p1, p2):
         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         ret,img_thresh = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
         pmid = Point2(int((p1.x + p2.x)/2),int((p1.y + p2.y)/2))
         pixelPresent = 1
         if img_thresh[(pmid.y)+1, (pmid.x)+1] == 0:
             pixelPresent +=1
         if img_thresh[(pmid.y)-1, (pmid.x)-1] == 0:
             pixelPresent +=1
         if img_thresh[(pmid.y)+2, (pmid.x)+2] == 0:
             pixelPresent +=1
         if img_thresh[(pmid.y)-2, (pmid.x)-2] == 0:
             pixelPresent +=1
         if pixelPresent == 4:
             if img_thresh[(pmid.y)+3, (pmid.x)+3] == 0 or img_thresh[(pmid.y)-3, (pmid.x)-3] == 0 :
                pixelPresent +=1

         return pixelPresent

    @staticmethod
    def EraseBox(img, p1, p2):
        P1 = (p1.x, p1.y)
        P2 = (p2.x, p2.y)
        cv2.rectangle(img, P1, P2, (255,255,255), -1)
        return img

    @staticmethod
    def EraseCircle(img, p1, radius):
         P1 = (int(p1.x), int(p1.y))
         Radius = (int(radius))
         cv2.circle(img, P1, Radius, (255,255,255),2) 
         return img


