# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
from Core.Features.LineSegments.LineSegmentsFeature import LineSegmentsFeature

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

global img, threshImg, imageCorner, imageHoughLine, imageOutput, imgHeight, imgWidth, imgChannels, blankImg  
global ArrowHeadsList

class DimensionalLinesFeature():

    @staticmethod
    def Detect(Feature_Manager):
        global make_dir_root, timestr, ArrowHeadsList
        make_dir_root = Feature_Manager._RootDirectory
        ExtractedArrows = Feature_Manager._DetectedArrowHead
        image = Feature_Manager._ImageOriginal.copy()
        ArrowHeadsList = ExtractedArrows
        LineSegmentsFeature.Make_Directory(make_dir_root) 
        LineSegmentsFeature.InitializeDimLine(image)
        cornerPts, cornerImageOutput, extractedLinesP, houghlineImageOutput = LineSegmentsFeature.EntityDetection()
        arrowPts = []
        for i in ExtractedArrows:
             pt = i._ArrowCenter
             arrowPts.append(pt)
        uniqueLines = LineSegmentsFeature.SegmentCreator(extractedLinesP)
        segLines = LineSegmentsFeature.SeggeratedCreator(uniqueLines)
        LineSegmentsFeature.cornerOnSegLine(arrowPts, segLines)
        detectedLineSegments = LineSegmentsFeature.DetectDimensionalLineSegments(segLines, ArrowHeadsList)
        DimensionalLineImage = LineSegmentsFeature.PlotLine(detectedLineSegments)
        LineSegmentsFeature.DisplayOutputs()
        cv2.imwrite(make_dir_root + "/DimensionalLine_Extraction_Output.png", DimensionalLineImage)
        
        return detectedLineSegments, DimensionalLineImage
    
    @staticmethod
    def Dump(make_dir_root, time, segments):
        Root = Element("Root")
        Extracted_DimensionalLine = SubElement(Root, "Extracted_DimensionalLine")
        i = 0
        for item in segments:
            Extracted_Dimension_Line = SubElement(Extracted_DimensionalLine, "Extracted_Dimension_Line")
            Extracted_Dimension_Line.text = str(i)
            for ar in item._ArrowHeads:
                Arrow_Head = SubElement(Extracted_Dimension_Line, "Arrow_Head")
                p1 = ar._BoundingBoxP1
                p2 = ar._BoundingBoxP2
                center = ar._ArrowCenter
                BB_Min_Point = SubElement(Arrow_Head, "BB_Min_Point")
                BB_Min_Point_X = SubElement(BB_Min_Point, "X")
                BB_Min_Point_X.text = str(p1.x)
                BB_Min_Point_Y = SubElement(BB_Min_Point, "Y")
                BB_Min_Point_Y.text = str(p1.y)

                BB_Max_Point = SubElement(Arrow_Head, "BB_Max_Point")
                BB_Max_Point_X = SubElement(BB_Max_Point, "X")
                BB_Max_Point_X.text = str(p2.x)
                BB_Max_Point_Y = SubElement(BB_Max_Point, "Y")
                BB_Max_Point_Y.text = str(p2.y)

                Centroid = SubElement(Arrow_Head, "Centroid")
                X_Point = SubElement(Centroid, "X")
                X_Point.text = str(center.x) 
                Y_Point = SubElement(Centroid, "Y")
                Y_Point.text = str(center.y) 

            for ls in item._Leaders:
                Segment = SubElement(Extracted_Dimension_Line, "Segment")
                Start_Point = SubElement(Segment, "Start_Point")
                Start_Point_X = SubElement(Start_Point, "X")
                Start_Point_X.text = str(ls.startPoint.x)
                Start_Point_Y = SubElement(Start_Point, "Y")
                Start_Point_Y.text = str(ls.startPoint.y)

                End_Point = SubElement(Segment, "End_Point")
                End_Point_X = SubElement(End_Point, "X")
                End_Point_X.text = str(ls.endPoint.x)
                End_Point_Y = SubElement(End_Point, "Y")
                End_Point_Y.text = str(ls.endPoint.y)
               
            i += 1
           
        tree = ET.ElementTree(Root)
        tree.write(make_dir_root +"/Dimensional_Line_Segment_Extraction.xml")
           
        