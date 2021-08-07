# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
from math import fabs
import numpy as np
from Core.Math.Point2 import Point2
from Core.Math.Line2 import Line2
from Core.Math.MathUtils import MathUtils
from Core.Features.Cognition.Cognition import Cognition
from Core.Features.FeatureManager import DimensionalLines

global img, threshImg, imageCorner, imageHoughLine, imageOutput, imgHeight, imgWidth, imgChannels, ArrowHeadsList,blankImg

class SpecialLineSegments:

    def __init__(self):
        self._p1 = Point2(0,0)
        self._p2 = Point2(0,0)
        self._line = Line2(self._p1, self._p2)
        self._lineSegments = []
        self._cornerPoints = []

    def __repr__(self):
        return "".join(["SpecialLineSegments[ (Line = ", str(self._line), "),(LineSegments = ", str(self._lineSegments), "),(CornerPoints = ", str(self._cornerPoints), ")]"])

    def ProjectCorners(self):
       corners = self._cornerPoints
       projCorners = []
       for cp in corners:
          pcp = MathUtils.ProjectToLine2(self._line.startPoint, self._line.endPoint, cp)
          projCorners.append(pcp)
       self._cornerPoints = projCorners

    def ProjectLineSegmentEnds(self):
       projLineSegments = []
       for ls in self._lineSegments:
          lss = ls.startPoint
          lse = ls.endPoint
          lssp = MathUtils.ProjectToLine2(self._line.startPoint, self._line.endPoint, lss)
          lsep = MathUtils.ProjectToLine2(self._line.startPoint, self._line.endPoint, lse)
          lsp = Line2(lssp, lsep)
          projLineSegments.append(lsp)
       self._lineSegments = projLineSegments

    def SortCorners(self):
       sortedCornersDict = {}
       corners = self._cornerPoints
       for cp in corners:
         u = SpecialLineSegments.GetUParam(cp,self)                  
         sortedCornersDict[u] = cp
       keys = sortedCornersDict.keys()
       sortedKeys = sorted(keys)
       sortedCorners = []
       for i in range(0, len(sortedKeys)):
          key = sortedKeys[i]
          corner = sortedCornersDict[key]
          sortedCorners.append(corner)
       self._cornerPoints = sortedCorners
       self.SetEnds()

    def SetEnds(self):
       points = []
       numCorners = len(self._cornerPoints)
       if numCorners >= 1:
            lsp1, lsp2 = SpecialLineSegments.SeggregatePoints(self._lineSegments, self._line)
            lsp1 = MathUtils.ProjectToLine2(self._line.startPoint, self._line.endPoint, lsp1)
            lsp2 = MathUtils.ProjectToLine2(self._line.startPoint, self._line.endPoint, lsp2)
            cs = self._cornerPoints[0]
            ce = self._cornerPoints[numCorners - 1]
            points.append(lsp1)
            points.append(lsp2)
            points.append(cs)
            points.append(ce)
            sortedEndPts = SpecialLineSegments.sortPoints(points, self._line)
            numPts = len(sortedEndPts)
            s = sortedEndPts[0]
            e = sortedEndPts[numPts - 1]
            line = Line2(s, e)
            self._line = line
    
    def listCorners(self):
        corners = self._cornerPoints
        listCorners = []
        line = self._line
        s = line.startPoint
        e = line.endPoint
        listCorners.append(s)
        listCorners.append(e)
        for cp in corners:
            listCorners.append(cp)

        self._cornerPoints = listCorners
        sortedpoints = SpecialLineSegments.sortPoints(self._cornerPoints, self._line)
        self._cornerPoints = sortedpoints


    @staticmethod
    def sortPoints(points, line):
        sortedPointsDict = {}
        for p in points:
          u = SpecialLineSegments.GetUParamLine(p,line)                 
          sortedPointsDict[u] = p
        keys = sortedPointsDict.keys()
        sortedKeys = sorted(keys)
        sortedPoints = []
        for i in range(0, len(sortedKeys)):
           key = sortedKeys[i]
           point = sortedPointsDict[key]
           sortedPoints.append(point)
        return sortedPoints

    @staticmethod
    def SeggregatePoints(linesegments, line):
        points = []
        for ls in linesegments:
            sPt = ls.startPoint
            ePt = ls.endPoint
            points.append(sPt)
            points.append(ePt)
        sortedSegPoints = SpecialLineSegments.sortPoints(points, line)
        p1 = sortedSegPoints[0]
        p2 = sortedSegPoints[(len(sortedSegPoints) - 1)]
        return p1, p2
    
    def CheckPixelsInVicinity(self,x, y, threshImg):
        imgHeight = threshImg.shape[0]
        imgWidth = threshImg.shape[1]
        scanRange = 3               
        if x < (imgWidth - scanRange) and y < (imgHeight - scanRange):
            for i in range(-scanRange, scanRange):
                for j in range(-scanRange, scanRange):
                    xj = int(x + j)
                    yi = int(y + i)
                    if threshImg[yi, xj] == 0:
                        return True
        return False

    def FindPercentageOfPointsOnLine(self, pointsOnLineBtnCorners):
      global threshImg
      TotalPixel = len(pointsOnLineBtnCorners)
      NonZeroPixel = 0
      for i in pointsOnLineBtnCorners:
          pixelPresent = self.CheckPixelsInVicinity(i[0], i[1], threshImg)
          if pixelPresent == True:
              NonZeroPixel += 1
              
      percent = float((100 * NonZeroPixel)/ TotalPixel)
      return percent

    @staticmethod
    def GetUParam(c1, sl):
       line = sl._line                                                    
       startpt = line.startPoint
       endpt = line.endPoint
       denominator = fabs(endpt.x - startpt.x)
       tolerance = 1.0
       U = 0
       if denominator < tolerance :
           U = float((c1.y - startpt.y) / (endpt.y - startpt.y))
       else:
           U = float((c1.x - startpt.x) / (endpt.x - startpt.x))
       return U

    @staticmethod
    def GetUParamLine(c1, sl):
       line = sl                                                    
       startpt = line.startPoint
       endpt = line.endPoint
       denominator = fabs(endpt.x - startpt.x)
       tolerance = 1.0
       U = 0
       if denominator < tolerance :
           U = float((c1.y - startpt.y) / (endpt.y - startpt.y))
       else:
           U = float((c1.x - startpt.x) / (endpt.x - startpt.x))
       return U

    @staticmethod
    def PixelScanner(p1, p2, img):
        
        height = img.shape[0]
        width = img.shape[1]
        p1x = p1.x
        p2x = p2.x
        p1y = p1.y
        p2y = p2.y

        horizontal_projection = p2x - p1x
        absolute_horizontal_projection = fabs(horizontal_projection)
        absolute_horizontal_projection = round(absolute_horizontal_projection)
        vertical_projection = p2y - p1y
        absolute_vertical_projection = fabs(vertical_projection)
        absolute_vertical_projection = round(absolute_vertical_projection)
        number = np.maximum(absolute_vertical_projection , absolute_horizontal_projection)
        line_pixel_array = np.empty(shape=(np.maximum(absolute_vertical_projection , absolute_horizontal_projection) , 3), dtype = np.float32)
        line_pixel_array.fill(np.nan)
        
        negative_Y = p1y > p2y
        negative_X = p1x > p2x
        if p1y == p2y: 
            line_pixel_array[ : , 1 ] = p1y
            if negative_X:
                line_pixel_array[ : , 0 ] = np.arange(p1x - 1 , p1x - absolute_horizontal_projection - 1 , -1)
            else:
                line_pixel_array[ : , 0 ] = np.linspace(p1x + 1 , p1x + absolute_horizontal_projection + 1 , number)
        elif p1x == p2x: 
            line_pixel_array[ : , 0 ] = p1x
            if negative_Y:
                line_pixel_array[ : , 1 ] = np.arange(p1y - 1 , p1y - absolute_vertical_projection - 1 , -1)
            else:
                line_pixel_array[ : , 1 ] = np.linspace(p1y + 1 , p1y + absolute_vertical_projection + 1 , number)
        else: 
            large_Slope = absolute_vertical_projection > absolute_horizontal_projection
            if large_Slope:
                slope = horizontal_projection.astype(np.float32) / vertical_projection.astype(np.float32)
                if negative_Y:
                    line_pixel_array[ : , 1 ] = np.arange(p1y - 1 , p1y - absolute_vertical_projection - 1 , -1)
                else:
                    line_pixel_array[ : , 1 ] = np.linspace(p1y + 1 , p1y + absolute_vertical_projection + 1, number)
                line_pixel_array[ : , 0 ] = (slope * (line_pixel_array[ : , 1] - p1y)).astype(np.int) + p1x         
            else:
                slope = vertical_projection.astype(np.float32) / horizontal_projection.astype(np.float32)
                if negative_X:
                    line_pixel_array[ : , 0 ] = np.arange(p1x - 1 , p1x - absolute_horizontal_projection - 1 , -1)
                else:
                    line_pixel_array[ : , 0] = np.linspace(p1x + 1, p1x + absolute_horizontal_projection + 1, num = number)
                line_pixel_array[ : , 1] = (slope * (line_pixel_array[ : , 0] - p1x)).astype(np.int) + p1y          

        X_Coordinate_Array = line_pixel_array[ : , 0]
        Y_Coordinate_Array = line_pixel_array[ : , 1]
        line_pixel_array = line_pixel_array[(X_Coordinate_Array >= 0) & (Y_Coordinate_Array >= 0) & (X_Coordinate_Array < width) & (Y_Coordinate_Array < height)]

        line_pixel_array[:,2] = img[line_pixel_array[:,1].astype(np.uint),line_pixel_array[:,0].astype(np.uint)]

        return line_pixel_array

    @staticmethod
    def ReturnArrowHeads(center):
        global ArrowHeadsList
    
        for a in ArrowHeadsList:
            arrow_center = a._ArrowCenter
            if fabs(int(arrow_center.x - center.x)) <= 5 and fabs(int(arrow_center.y - center.y)) <= 5:     
                a._ArrowCenter = center
                return a
        return None

    @staticmethod
    def CheckArrowOverlap(arrowHead):
        global ArrowHeadsList

        for a in ArrowHeadsList:
            if fabs(arrowHead._ArrowCenter.x - a._ArrowCenter.x) > 1 or fabs(arrowHead._ArrowCenter.y != a._ArrowCenter.y) > 1:
                overlap = Cognition.CheckOverlapByLineSegment(arrowHead._BoundingBoxP1, arrowHead._BoundingBoxP2, a._BoundingBoxP1, a._BoundingBoxP2)
                if overlap == True:
                    return True
        return False

    @staticmethod
    def CheckArrowOverlapBetweenTwo(a1, a2):
        if a1._ArrowCenter.x != a2._ArrowCenter.x or a1._ArrowCenter.y != a2._ArrowCenter.y:
                overlap = Cognition.CheckOverlapByLineSegment(a1._BoundingBoxP1, a1._BoundingBoxP2, a2._BoundingBoxP1, a2._BoundingBoxP2)
                if overlap == True:
                    return True
        return False

    def DetectDimensionalLineSegments(self, im, arrowlist):
       global img, threshImg, ArrowHeadsList
       ArrowHeadsList = arrowlist
       img = im
       gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       ret, threshImg = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
       numCorners = len(self._cornerPoints)
       ExtractedDimensionalLine = []
     
       if numCorners == 1:
              c1 = self._cornerPoints[0]
              c2 = self._line.startPoint
              c3 = self._line.endPoint
              for c in (c2,c3):
                Dimensional_LS = []
                Dimensional_AH = []
                if int(fabs(c1.x - c.x)) >= 3 or int(fabs(c1.y - c.y)) >= 3:
                    pointsOnLineBtnCorners = SpecialLineSegments.PixelScanner(c1, c, threshImg)
                    onlinePointsPercentage = self.FindPercentageOfPointsOnLine(pointsOnLineBtnCorners)
                    if onlinePointsPercentage > 90:
                        newlineSegm = Line2(c1,c)
                        if int(newlineSegm.Length()) > 8:                       
                            arrowHead = SpecialLineSegments.ReturnArrowHeads(c1)
                            if arrowHead is None:
                                continue
                            overlap = SpecialLineSegments.CheckArrowOverlap(arrowHead)       
                            if overlap == False:                                        
                                Dimensional_AH.append(arrowHead)
                                Dimensional_LS.append(newlineSegm)
                                DL = DimensionalLines()
                                DL.ExtractDimensionalLine(DL, Dimensional_AH, Dimensional_LS)
                                ExtractedDimensionalLine.append(DL)
        
       else:
             for i in range(0, numCorners-1):
                    Dimensional_LS = []
                    Dimensional_AH = []
                    c1 = self._cornerPoints[i]
                    c2 = self._cornerPoints[i+1]
                    if int(fabs(c1.x - c2.x)) >= 3 or int(fabs(c1.y - c2.y)) >= 3 :                
                        pointsOnLineBtnCorners = SpecialLineSegments.PixelScanner(c1, c2, threshImg)
                        onlinePointsPercentage = self.FindPercentageOfPointsOnLine(pointsOnLineBtnCorners)
                        if onlinePointsPercentage > 90:
                            newlineSegm = Line2(c1,c2)
                            if int(newlineSegm.Length()) > 8:                   
                                arrowHead1 = SpecialLineSegments.ReturnArrowHeads(c1)
                                arrowHead2 = SpecialLineSegments.ReturnArrowHeads(c2)
                                if arrowHead1 is None or arrowHead2 is None:
                                    continue
                                overlap = SpecialLineSegments.CheckArrowOverlapBetweenTwo(arrowHead1, arrowHead2)    
                                if overlap == False:  
                                    Dimensional_LS.append(newlineSegm)
                                    Dimensional_AH.append(arrowHead1)
                                    Dimensional_AH.append(arrowHead2)
                                    DL = DimensionalLines()
                                    DL.ExtractDimensionalLine(DL, Dimensional_AH, Dimensional_LS)
                                    ExtractedDimensionalLine.append(DL)
       return ExtractedDimensionalLine

    def DetectLineSegments(self):
       detectedLineSegments = []
       global img, threshImg
       gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       ret, threshImg = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

       numCorners = len(self._cornerPoints)
       if numCorners == 1:
              c1 = self._line.startPoint
              c2 = self._line.endPoint
              pointsOnLineBtnCorners = SpecialLineSegments.PixelScanner(c1, c2, threshImg)
              onlinePointsPercentage = self.FindPercentageOfPointsOnLine(pointsOnLineBtnCorners)
              if onlinePointsPercentage > 90:
                    newlineSegm = Line2(c1,c2)
                    if int(newlineSegm.Length()) > 6:           
                        detectedLineSegments.append(newlineSegm)
       else:

             for i in range(0, numCorners-1):
                
                c1 = self._cornerPoints[i]
                c2 = self._cornerPoints[i+1]
                if int(fabs(c1.x - c2.x)) >= 3 or int(fabs(c1.y - c2.y)) >= 3 :                
                    pointsOnLineBtnCorners = SpecialLineSegments.PixelScanner(c1, c2, threshImg)
                    onlinePointsPercentage = self.FindPercentageOfPointsOnLine(pointsOnLineBtnCorners)
                    if onlinePointsPercentage > 90:
                        newlineSegm = Line2(c1,c2)
                        if int(newlineSegm.Length()) > 6:           
                            detectedLineSegments.append(newlineSegm)
       return detectedLineSegments
