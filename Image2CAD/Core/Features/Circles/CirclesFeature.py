# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:39:29 2020

@author: Aditya Intwala
"""


import cv2
import numpy as np
from scipy import optimize
from math import fabs
from Core.Math import Point2
from Core.Features.FeatureManager import ExtractedCircles

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

class CirclesFeature():

    global make_dir_root, timestr, threshImg, ImgHeight, ImgWidth, ImgChannels

    @staticmethod
    def Detect(Feature_Manager):
        global make_dir_root, threshImg
        make_dir_root = Feature_Manager._RootDirectory
        img = Feature_Manager._ImageCleaned.copy() 
        Output_img = Feature_Manager._ImageOriginal.copy()

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, threshImg = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        contours = CirclesFeature.preprocess(img)
        DetectedCircles = CirclesFeature.fitting(img, contours)
        DetectedCircles = CirclesFeature.UniqueCircles(DetectedCircles)
        RequiredCircles = CirclesFeature.circleFiltering(DetectedCircles)
        Img_Circle = CirclesFeature.drawCircle(Output_img, RequiredCircles)

        return RequiredCircles, Img_Circle
    
    @staticmethod
    def Dump(make_dir_root, time, DetectedCircle):
        Root = Element("Root")
        Extracted_Circle = SubElement(Root, "Extracted_Circle")
        i = 0
        for item in DetectedCircle:
            Circle = SubElement(Extracted_Circle, "Circle")
            Circle.text = str(i)
            Centre = SubElement(Circle, "Centre")
            X_coordinate = SubElement(Centre, "x")
            X_coordinate.text = str(item._centre.x)
            Y_coordinate = SubElement(Centre, "y")
            Y_coordinate.text = str(item._centre.y)
            Radius = SubElement(Circle, "Radius")
            Radius.text = str(item._radius)
            i += 1
           
        tree = ET.ElementTree(Root)
        tree.write(make_dir_root +"/Circle_Extraction.xml")
  
    @staticmethod
    def preprocess(img):
        global ImgHeight, ImgWidth, ImgChannels
        ImgHeight, ImgWidth, ImgChannels = img.shape
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img_thresh = cv2.threshold(img_gray,0,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        ret, contours, hierarchy = cv2.findContours(img_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)     #RETR_CCOMP
        return contours

    @staticmethod
    def fitting(img, contours):
        global ImgHeight, ImgWidth, ImgChannels
        DetectedCircles = []
        for c in contours:
            if len(c) >=3 :
                Fit_Circle = CurveFitting.CircleFitting(img,c)

                if Fit_Circle is not None:
                    if int(Fit_Circle[0][0]) < ImgWidth and int(Fit_Circle[0][1]) < ImgHeight and 6 < int(Fit_Circle[1]) < 300:
                         cir = (int(Fit_Circle[0][0]),int(Fit_Circle[0][1]), int(Fit_Circle[1]))
                         DetectedCircles.append(cir)

        return DetectedCircles
        
    @staticmethod
    def circleFiltering(DetectedCircles):
        ThresholdPixel = 4
        RequiredCircles = []
        UnwantedCircles = []
        
        for i in range(0,len(DetectedCircles)):
            c1 = DetectedCircles[i]
            c1 = (int(c1[0]), int(c1[1]), int(c1[2]))
            if c1 not in UnwantedCircles:
                if c1 not in RequiredCircles:
                    if len(RequiredCircles) != 0:
                        IsInRequiredCircles = []
                        for j in RequiredCircles:
                                if fabs(j[0]-c1[0]) < ThresholdPixel and fabs(j[1]-c1[1]) < ThresholdPixel and fabs(j[2]-c1[2]) < ThresholdPixel:
                                    IsInRequiredCircles.append(True)
                                else:
                                    IsInRequiredCircles.append(False)
                        if True in IsInRequiredCircles:
                                continue
                        else:
                             nc = (int(c1[0]),int(c1[1]),int(c1[2]))
                             RequiredCircles.append(nc)
                    else:
                        nc = (int(c1[0]),int(c1[1]),int(c1[2]))
                        RequiredCircles.append(nc)

            for c in range(i+1,len(DetectedCircles)):
                c2 = DetectedCircles[c]
                c2 = (int(c2[0]), int(c2[1]), int(c2[2]))

                if c2 not in UnwantedCircles:
                    if fabs(c1[0]-c2[0]) < ThresholdPixel and fabs(c1[1]-c2[1]) < ThresholdPixel and fabs(c1[2]-c2[2]) < ThresholdPixel:
                        IsInRequiredCircles = []
                        if len(RequiredCircles) > 0:
                            for j in RequiredCircles:
                                if fabs(j[0]-c2[0]) < ThresholdPixel and fabs(j[1]-c2[1]) < ThresholdPixel and fabs(j[2]-c2[2]) < ThresholdPixel:
                                    IsInRequiredCircles.append(True)
                                else:
                                    IsInRequiredCircles.append(False)

                            if True in IsInRequiredCircles:
                                continue
                            else:
                                nx = int((fabs(c1[0]+c2[0]))/2)
                                ny = int((fabs(c1[1]+c2[1]))/2)
                                nr = int((fabs(c1[2]+c2[2]))/2)
                                nc = (int(nx),int(ny),int(nr))
                                RequiredCircles.append(nc)
                                UnwantedCircles.append(c1)
                                UnwantedCircles.append(c2)

                        else:
                                nx = int((fabs(c1[0]+c2[0]))/2)
                                ny = int((fabs(c1[1]+c2[1]))/2)
                                nr = int((fabs(c1[2]+c2[2]))/2)
                                nc = (int(nx),int(ny),int(nr))
                                RequiredCircles.append(nc)
                                UnwantedCircles.append(c1)
                                UnwantedCircles.append(c2)

                    else:
                        IsInRequiredCircles = []
                        for j in RequiredCircles:
                                if fabs(j[0]-c1[0]) < ThresholdPixel and fabs(j[1]-c1[1]) < ThresholdPixel and fabs(j[2]-c1[2]) < ThresholdPixel:
                                    IsInRequiredCircles.append(True)
                                else:
                                    IsInRequiredCircles.append(False)
                        if True in IsInRequiredCircles:
                                continue
                        else:
                             nc = (int(c1[0]),int(c1[1]),int(c1[2]))
                             RequiredCircles.append(nc)
        RequiredCirclesExtracted = []
        for i in RequiredCircles:
            EC = ExtractedCircles()
            centre = Point2(i[0], i[1])
            radius = i[2]
            EC.ExtractCircle(EC,centre, radius)
            RequiredCirclesExtracted.append(EC)
        
        return RequiredCirclesExtracted

    @staticmethod
    def drawCircle(img, RequiredCircles):
        for i in RequiredCircles:
            c = i._centre
            r = i._radius
            cv2.circle(img,(int(c.x),int(c.y)), int(r), (0,0,255),1)
        cv2.imwrite(make_dir_root +"/Circle_Extraction_Output.png",img)
        return img

    @staticmethod
    def circleScanner(center, radius):
        switch = 3 - (2 * radius)
        points = set()
        x = 0
        y = radius
        while x <= y:
            points.add((x+center[0],-y+center[1]))
            points.add((y+center[0],-x+center[1]))
            points.add((y+center[0],x+center[1]))
            points.add((x+center[0],y+center[1]))
            points.add((-x+center[0],y+center[1]))        
            points.add((-y+center[0],x+center[1]))
            points.add((-y+center[0],-x+center[1]))
            points.add((-x+center[0],-y+center[1]))
            if switch < 0:
                switch = switch + (4 * x) + 6
            else:
                switch = switch + (4 * (x - y)) + 10
                y = y - 1
            x = x + 1
        return points

    @staticmethod
    def CheckPixelsInVicinity(x, y, threshImg):
        scanRange = 2
        for i in range(-scanRange, scanRange):
            for j in range(-scanRange, scanRange):
                xj = x + j
                yi = y + i
                if threshImg[yi, xj] == 0:
                    return True
        return False

    @staticmethod
    def UniqueCircles(detectedcircles):
        global threshImg, ImgHeight, ImgWidth, ImgChannels
        DetectedCircles = []

        for i in detectedcircles:
            if i[0] <= ImgWidth and i[1] <= ImgHeight:
                points = CirclesFeature.circleScanner((int(i[0]),int(i[1])),int(i[2]))
                total = len(points)
                nonzero = 0
                for p in points:
                    if 2 <= p[0] <= (ImgWidth - 2) and 2 <= p[1] <= (ImgHeight - 2):
                        pixelpresent = CirclesFeature.CheckPixelsInVicinity(p[0], p[1], threshImg)
                        if pixelpresent == True:
                            nonzero += 1
                percent = (100 * nonzero)/ total
                if percent > 50:
                    c = (int(i[0]), int(i[1]), int(i[2]))
                    DetectedCircles.append(c)
        return DetectedCircles    
    
    
    
class CurveFitting():
    @staticmethod
    def CircleFitting(img,contour):
         ImgHeight, ImgWidth, ImgChannels = img.shape
         x = []
         y = []
         for i in contour:
             xpt = i[0][0]
             ypt = i[0][1]
             x.append(xpt)
             y.append(ypt)
         RANSAC_parameter={'eps': 3, 'ransac_threshold': 0.05,'nIter': 100, 'lowerRadius': 5, 'upperRadius': 500 }
         fit = []
         for ii in range(RANSAC_parameter['nIter']):
             randPoints = np.random.permutation(len(x))[:3]
             X = [x[randPoints[0]],x[randPoints[1]],x[randPoints[2]]]
             Y = [y[randPoints[0]],y[randPoints[1]],y[randPoints[2]]]
             (center, radius) = CurveFitting.fit_circle(X, Y)
             if not (RANSAC_parameter['lowerRadius'] < radius < RANSAC_parameter['upperRadius'] and 0 <= center[0] < ImgWidth and 0 <= center[1] < ImgHeight):
                 continue 
             centerDistance = np.sqrt((x-center[0])**2 + (y-center[1])**2)
             inCircle = np.where(np.abs(centerDistance-radius)<RANSAC_parameter['eps'])[0]
             inPts = len(inCircle)
             if inPts < RANSAC_parameter['ransac_threshold'] *4*np.pi*radius*RANSAC_parameter['eps'] or inPts < 3:
                 continue
             xpt = []
             ypt = []
             
             for i in inCircle:
                 xpt.append(x[i])
                 ypt.append(y[i]) 
             (center, radius) = CurveFitting.fit_circle(xpt, ypt)
             fitC = (center, radius, inPts)
             fit.append(fitC)

         if len(fit)!=0:    
            sortedFit = sorted(fit, key = lambda fit: fit[2], reverse = True)
            fitBestCircle = sortedFit[0]

         else:
             return None
         return fitBestCircle

    @staticmethod
    def calc_dist(x,y,xc, yc):
        return np.sqrt((x-xc)**2 + (y-yc)**2)

    @staticmethod
    def fit_circle(xPts,yPts):
        x_m = np.mean(xPts)
        y_m = np.mean(yPts)
        
        def calc_R(xc, yc):
            return np.sqrt((xPts-xc)**2 + (yPts-yc)**2)
                
        def f_2(c):
            Ri = calc_R(*c)
            return Ri - Ri.mean()
        
        center_estimate = x_m, y_m
        center, ier = optimize.leastsq(f_2, center_estimate)
        xc, yc = center
        Ri       = calc_R(xc, yc)
        R        = Ri.mean()
        return (center, R ) 


    
    