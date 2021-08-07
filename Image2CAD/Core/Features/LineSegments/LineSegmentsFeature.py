# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
import numpy as np
from Core.Math.Point2 import Point2
from Core.Math.Line2 import Line2
from Core.Features.LineSegments.SpecialLineSegments import SpecialLineSegments
from Core.Features.Cognition.Cognition import Cognition
from Core.Features.FeatureManager import ExtractedLines

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

global img, threshImg, imageCorner, imageHoughLine, imageOutput, imgHeight, imgWidth, imgChannels, ArrowHeadsList,blankImg

class LineSegmentsFeature():
    global make_dir_root, timestr, DManager
    
    @staticmethod
    def IsCollinear(l, ls):
       startPtOnLine = l.OnLine(ls.startPoint)
       endPtOnLine = l.OnLine(ls.endPoint)
       if startPtOnLine == True and endPtOnLine == True:
          return True
       return False

    @staticmethod
    def CollinearLineExists(lineDict, ls):
       lines = lineDict.keys()
       for l in lines:
         if LineSegmentsFeature.IsCollinear(l, ls):
            return l
       return None

    @staticmethod
    def GetUniqueLines(lineSegments):
       lines = {}
       for i in range(1, len(lineSegments)):
         ls = lineSegments[i]
         cl = LineSegmentsFeature.CollinearLineExists(lines, ls)
         if None == cl:
            temp = Line2(ls.startPoint, ls.endPoint)
            if temp.IsDegenerate() == False:
               lines[temp] = []
               lines[temp].append(ls)
         else:
             lines[cl].append(ls)
       
       return lines

    @staticmethod
    def DetectLineSegments(segLines):
       lineSegmentsDetected = []
       for sl in segLines:
          sl.ProjectCorners()
          sl.SortCorners()
          sl.ProjectLineSegmentEnds()
          sl.listCorners()
          lineSegments = sl.DetectLineSegments()
          lineSegmentsDetected.append(lineSegments)
       return lineSegmentsDetected

    @staticmethod
    def DetectDimensionalLineSegments(segLines, ArrowHeadList):
       global ArrowHeadsList
       ArrowHeadsList = ArrowHeadList
       lineSegmentsDetected = []
       for sl in segLines:
          sl.ProjectCorners()
          sl.SortCorners()
          sl.ProjectLineSegmentEnds()
          lineSegments = sl.DetectDimensionalLineSegments(img, ArrowHeadsList)
          if len(lineSegments) != 0:
              for l in lineSegments:
                    lineSegmentsDetected.append(l)
       return lineSegmentsDetected

    @staticmethod
    def Initialize(image):
        global img, imageCorner, imageHoughLine, imageOutput, imgHeight, imgWidth, imgChannels, DManager 
        img = image
        imgHeight, imgWidth, imgChannels = img.shape
        imageOutput = DManager._ImageOriginal.copy()
        imageCorner = img.copy()
        imageHoughLine = img.copy()

    @staticmethod
    def InitializeDimLine(image):
        global img, imageCorner, imageHoughLine, imageOutput, imgHeight, imgWidth, imgChannels
        img = image
        imgHeight, imgWidth, imgChannels = img.shape
        imageOutput = img.copy()
        imageCorner = img.copy()
        imageHoughLine = img.copy()

    
    @staticmethod        
    def HoughLineP(img, rho, theta, threshold, minLineLength, maxLineGap):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 50, 150, apertureSize = 3)

        lines = cv2.HoughLinesP(canny, int(rho), float(theta), int(threshold), int(minLineLength), int(maxLineGap))
        extractedLines = []
        if None != lines.any():
            for line in lines:
                for x1,y1,x2,y2 in line:
                    p1 = Point2(x1,y1)
                    p2 = Point2(x2,y2)
                    ex = ExtractedLines()
                    ex.ExtractLine(ex,rho, theta, p1, p2)
                    extractedLines.append(ex)
                    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 1)

 
        return extractedLines, img
    
    @staticmethod
    def CornerShiTomasai (img, numCorners, qualityOfCorner, minElucDistance, useHarris):
        image = img
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        corners = cv2.goodFeaturesToTrack(gray, numCorners, qualityOfCorner, minElucDistance, useHarrisDetector = useHarris)
        corners = np.int0(corners)

        points = []
        for i in corners:
            x,y = i.ravel()
            cv2.circle(image,(x,y), 2, (0,60,255),-1)
            points.append(Point2(x, y))
        
        return points,image
    
    @staticmethod
    def EntityDetection():
        global imageCorner, imageHoughLine
        (cornerPts, cornerImageOutput) = LineSegmentsFeature.CornerShiTomasai(imageCorner, 200, 0.01, 10, True)
        (extractedLinesP, houghlineImageOutput) = LineSegmentsFeature.HoughLineP(imageHoughLine, 1.0, 0.00872, 10, 10, 5)
        return cornerPts, cornerImageOutput, extractedLinesP, houghlineImageOutput

    @staticmethod
    def SegmentCreator(extractedLinesP):

        lineSegments = []
        for el in extractedLinesP:
           ls = Line2(el._p1, el._p2)
           lineSegments.append(ls)

        uniqueLines = LineSegmentsFeature.GetUniqueLines(lineSegments)
        return uniqueLines

    @staticmethod
    def SeggeratedCreator(uniqueLines):
        segLines = []
        for lkey in uniqueLines.keys():
           l = lkey
           lineSegments = uniqueLines[lkey]
           sl = SpecialLineSegments()
           sl._line = l;
           sl._lineSegments = lineSegments
           sl._cornerPoints = []
           segLines.append(sl)
        return segLines

    @staticmethod
    def cornerOnSegLine(cornerPts, segLines):
        for cp in cornerPts:
           for sl in segLines:
              line = sl._line
              if line.OnLine(cp) == True:
                  sl._cornerPoints.append(cp)
        
    
    @staticmethod
    def DrawLines(detectedLineSegments):
        global imageOutput, blankImg
        for i in detectedLineSegments:
            for ls in i:
                p1 = ls.startPoint
                p2 = ls.endPoint
                cv2.line(imageOutput, (int(p1.x),int(p1.y)), (int(p2.x), int(p2.y)), (255,0,0), 1)  
        return imageOutput                        

    @staticmethod
    def PlotLine(detectedLineSegments):
        global imageOutput, img, blankImg
        for i in detectedLineSegments:
            ls = i._Leaders
            for l in ls:
                p1 = l.startPoint
                p2 = l.endPoint
                cv2.line(imageOutput, (int(p1.x),int(p1.y)), (int(p2.x), int(p2.y)), (255,0,0), 1)
        return imageOutput

    @staticmethod
    def DisplayOutputs():
        global imageCorner, imageHoughLine, imageOutput, make_dir_root,blankImg
        cv2.imwrite(make_dir_root + "/Line_Extraction_Output.png",imageOutput)
         

    @staticmethod
    def Make_Directory(makedir_root):
        global make_dir_root
        make_dir_root = makedir_root

    @staticmethod
    def Remove_Empty(detectedLineSegments):
        Segments = []
        for ls in detectedLineSegments:
            if len(ls) !=0 :
                for l in ls:
                    Segments.append(l)
        return Segments

    @staticmethod
    def Remove_EmptyLS(detectedLineSegments):
        Segments = []
        for ls in detectedLineSegments:
            if len(ls) !=0 :
                Segments.append(ls)
        return Segments

       
    @staticmethod
    def Detect(Feature_Manager):
        global make_dir_root, timestr, DManager
        DManager = Feature_Manager
        make_dir_root = Feature_Manager._RootDirectory
        image = Feature_Manager._ImageCleaned.copy()
        
        LineSegmentsFeature.Initialize(image)
        
        cornerPts, cornerImageOutput, extractedLinesP, houghlineImageOutput = LineSegmentsFeature.EntityDetection()
        
        uniqueLines = LineSegmentsFeature.SegmentCreator(extractedLinesP)
        
        segLines = LineSegmentsFeature.SeggeratedCreator(uniqueLines)
        
        LineSegmentsFeature.cornerOnSegLine(cornerPts, segLines)
        
        detectedLineSegments = LineSegmentsFeature.DetectLineSegments(segLines)
        
        Segments = Cognition.MergeLineSegments(detectedLineSegments)
        
        LineImg = LineSegmentsFeature.DrawLines(Segments)
        
        LineSegmentsFeature.DisplayOutputs()
        
        
        return Segments, LineImg
    
    
    @staticmethod
    def Dump(make_dir_root, segments):
        Root = Element("Root")
        Extracted_Line_Segments = SubElement(Root, "Extracted_Line_Segments")
        i = 0
        for item in segments:
            Extracted_Segment = SubElement(Extracted_Line_Segments, "Extracted_Segment")
            Extracted_Segment.text = str(i)
            Start_Point = SubElement(Extracted_Segment, "Start_Point")
            Start_Point_x = SubElement(Start_Point, "x")
            Start_Point_x.text = str(item.startPoint.x)
            Start_Point_y = SubElement(Start_Point, "y")
            Start_Point_y.text = str(item.startPoint.y)
            End_Point = SubElement(Extracted_Segment, "End_Point")
            End_Point_x = SubElement(End_Point, "x")
            End_Point_x.text = str(item.endPoint.x)
            End_Point_y = SubElement(End_Point, "y")
            End_Point_y.text = str(item.endPoint.y)
            i += 1
           
        tree = ET.ElementTree(Root)
        tree.write(make_dir_root +"/Line_Segment_Extraction.xml")


        
        
