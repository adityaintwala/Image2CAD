# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
import numpy as np
from Core.Math.Point2 import Point2
from Core.Features.FeatureManager import ArrowHeads

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

class ArrowHeadsFeature():

    @staticmethod
    def Detect(Feature_Manager):
        img = Feature_Manager._ImageOriginal.copy()
        
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret2,Threshold = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        
        kernel = np.ones((2,2),np.uint8)
        blackhat = cv2.morphologyEx(Threshold, cv2.MORPH_BLACKHAT, kernel)

        InvThreshold = cv2.bitwise_not(Threshold)
        NewImg = InvThreshold - blackhat

        arrows_image = NewImg.copy()
        kernel = np.ones((3,3),np.uint8)
        erosion = cv2.erode(arrows_image, kernel)
        dilated = cv2.dilate(erosion, kernel)
        
        _im,contour,hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        empty_image = erosion.copy()
        empty_image.fill(0)
        ExtractedArrows = []
   
        for i in range(0, len(contour)):
            area = cv2.contourArea(contour[i])

            if (area > 35 and area <= 70): 
                x,y,w,h = cv2.boundingRect(contour[i])
                P1 = Point2(int(x-3), int(y-3))
                P2 = Point2(int(x+w+2), int(y+h+2))
                cv2.rectangle(img,(x-3,y-3),(x+w+2,y+h+2),(255,0,0),1)
                M = cv2.moments(contour[i])
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                c = Point2(cx,cy)
                ar = ArrowHeads()
                ar.ExtractArrowHead(ar, P1, P2, c)
                ExtractedArrows.append(ar)
                cv2.circle(img, (cx,cy), 1, (0,255,0), 1)
        make_dir_root = Feature_Manager._RootDirectory
        cv2.imwrite(make_dir_root +"/Arrowheads_Extraction_Output.png",img)
        return ExtractedArrows, img
    
    
    @staticmethod
    def Dump(make_dir_root, DetectedArrows):
        Root = Element("Root")
        Extracted_Arrows = SubElement(Root, "Extracted_Arrows")
        i = 0
        for item in DetectedArrows:
            Arrow = SubElement(Extracted_Arrows, "Arrow")
            Arrow.text = str(i)
            BB_Min_Point = SubElement(Arrow, "BB_Min_Point")
            Min_Point_x = SubElement(BB_Min_Point, "x")
            Min_Point_x.text = str(item._BoundingBoxP1.x)
            Min_Point_y = SubElement(BB_Min_Point, "y")
            Min_Point_y.text = str(item._BoundingBoxP1.y)
            BB_Max_Point = SubElement(Arrow, "BB_Max_Point")
            Max_Point_x = SubElement(BB_Max_Point, "x")
            Max_Point_x.text = str(item._BoundingBoxP2.x)
            Max_Point_y = SubElement(BB_Max_Point, "y")
            Max_Point_y.text = str(item._BoundingBoxP2.y)
            Centre_Point = SubElement(Arrow, "Centre_Point")
            Centre_Point_x = SubElement(Centre_Point, "x")
            Centre_Point_x.text = str(item._ArrowCenter.x)
            Centre_Point_y = SubElement(Centre_Point, "y")
            Centre_Point_y.text = str(item._ArrowCenter.y)
            i += 1
           
        tree = ET.ElementTree(Root)
        tree.write(make_dir_root +"/Arrow_Extraction.xml")
    
    