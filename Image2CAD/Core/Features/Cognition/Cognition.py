# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from Core.Math.Point2 import Point2
from Core.Math.Line2 import Line2
from Core.Math.MathUtils import MathUtils
from Core.Math.Constants import Constants
import cv2
import numpy as np
import operator
from math import sqrt, fabs, atan2
import collections
import sys
from Core.Features.FeatureManager import Dimensions, CorrelatedEntity
from Core.Utils.ImgTransform import ImgTransform


class Cognition():

    @staticmethod
    def GetUParam(c1, line):
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
    def angle_trunc(a):
        while a < 0.0:
            a += Constants.PI * 2
        return a
    
    @staticmethod
    def getAngleBetweenLineAndAxis(p1,p2):
        line = Line2(p1,p2)
        up1 = Cognition.GetUParam(p1,line)
        up2 = Cognition.GetUParam(p2,line)
        if up2 > up1:
            deltaY = p2.y - p1.y
            deltaX = p2.x - p1.x
        else:
            deltaY =  - p1.y - p2.y
            deltaX =  - p1.x - p2.x
        radians = Cognition.angle_trunc(atan2(deltaY, deltaX))
        degrees = MathUtils.RadToDeg(radians)
        degrees = (360 - degrees)
        return degrees

    @staticmethod
    def CheckForCoincidentLineSegments( p1, p2, p3, p4):
        v = p4 - p3
        w = p1 - p3
        w2 = p2 - p3
        if (v.i != 0):
            t0 = (w.i / v.i)
            t1 = (w2.i / v.i)
        else:
            t0 = (w.j / v.j)
            t1 = (w2.j / v.j)
        if (t0 > t1):
            t = t0
            t0 = t1
            t1 = t
        if (t0 > 1 or t1 < 0):
            return False
        return True

    @staticmethod
    def CheckIfIntersectingLineSegment(p1, p2, p3, p4):
        tolerance = Constants.PRECISION
        Pixeltolerance = 0.5 
        x1 = p1.x
        x2 = p2.x
        x3 = p3.x
        x4 = p4.x
        y1 = p1.y
        y2 = p2.y
        y3 = p3.y
        y4 = p4.y
        numeratorA = ((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))
        numeratorB = ((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))
        denominator = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))

        if (MathUtils.EQTF(denominator, 0.0, tolerance)):
            if(MathUtils.EQTF(numeratorB, 0.0, tolerance) and MathUtils.EQTF(numeratorA, 0.0, tolerance)):
                return Cognition.CheckForCoincidentLineSegments(p1, p2, p3, p4)
            return False                 
        ua = numeratorA / denominator
        ub = numeratorB / denominator

        if((ua > (0.0 - Pixeltolerance)) and (ua < (1.0 + Pixeltolerance)) and (ub > (0.0 - Pixeltolerance)) and (ub < (1.0 + Pixeltolerance))):
            return True
        return False

    @staticmethod
    def CheckIfOverlap(BB1_P1, BB1_P2, BB2_P1, BB2_P2):
        if BB1_P2.x < BB2_P1.x or BB2_P2.x < BB1_P1.x or BB1_P2.y < BB2_P1.y or BB2_P2.y < BB1_P1.y:
            return False
        return True

    @staticmethod
    def CheckOverlapByLineSegment(B1_P1, B1_P2, B2_P1, B2_P2):
        Ap1 = Point2(B1_P1.x, B1_P1.y)
        Ap2 = Point2(B1_P2.x, B1_P1.y)
        Ap3 = Point2(B1_P2.x, B1_P2.y)
        Ap4 = Point2(B1_P1.x, B1_P2.y)

        Bp1 = Point2(B2_P1.x, B2_P1.y)
        Bp2 = Point2(B2_P2.x, B2_P1.y)
        Bp3 = Point2(B2_P2.x, B2_P2.y)
        Bp4 = Point2(B2_P1.x, B2_P2.y)

        A_Segments = [Line2(Ap1, Ap2), Line2(Ap2, Ap3), Line2(Ap3, Ap4), Line2(Ap4, Ap1)]
        B_Segments = [Line2(Bp1, Bp2), Line2(Bp2, Bp3), Line2(Bp3, Bp4), Line2(Bp4, Bp1)]

        for i in A_Segments:
            p1 = i.startPoint
            p2 = i.endPoint
            for j in B_Segments:
                p3 = j.startPoint
                p4 = j.endPoint
                Intersects = Cognition.CheckIfIntersectingLineSegment(p1, p2, p3, p4)
                if Intersects == True:
                    return True
        return False
        
    @staticmethod
    def CheckIfOverlapLineSegments(Rect1_Segments, Rect2_Segments):
        for i in Rect1_Segments:
            p1 = i.startPoint
            p2 = i.endPoint
            for j in Rect2_Segments:
                p3 = j.startPoint
                p4 = j.endPoint
                Intersects = MathUtils.Check_Intersects_LineSegmentLineSegment(p1, p2, p3, p4)
                if Intersects == True:
                    return True
        return False

    @staticmethod
    def CollisionSegmentBox(bbMin, bbMax, startPt, endPt):
        direction = endPt - startPt
        direction = direction.Normalize()
        divx = 1 / direction.i
        if (divx >= 0):
            tminX = (bbMin.x - startPt.x) * divx
            tmaxX = (bbMax.x - startPt.x) * divx
        else:
            tminX = (bbMax.x - startPt.x) * divx
            tmaxX = (bbMin.x - startPt.x) * divx
        
        tmin = max(tminX,tmaxX)
        tmax = min(tminX, tmaxX)

        divy = 1 / direction.j
        if (divy >= 0):
            tminY = (bbMin.y - startPt.y) * divy
            tmaxY = (bbMax.y - startPt.y) * divy
        else:
            tminY = (bbMax.y - startPt.y) * divy
            tmaxY = (bbMin.y - startPt.y) * divy
        
        tmin = max(tmin, min(tmaxY,tminY))
        tmax = min(tmax, max(tmaxY,tminY))

        return tmax >= tmin

    @staticmethod
    def LineEquation(p1, p2):
        slope = (p2.y - p1.y) / (p2.x - p1.x)
        c = p1.y - (slope * p1.x)
        return slope, c  
    
    @staticmethod
    def LineCoefficients(p1, p2):
        A = p2.y - p1.y
        B = p1.x - p2.x
        C = (A * p1.x) + (B * p1.y)
        return A, B, C 

    @staticmethod
    def SortPointsByUParam(points, line):
        sortedPointsDict = {}
        for p in points:
          u = Cognition.GetUParam(p,line)                  #
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
    def SortDictionary(d):
        od = collections.OrderedDict(sorted(d.items()))
        return od

    @staticmethod
    def GetOrientation(Dimensionallines,BB):
        text_P1 = Point2(BB[0]-5,BB[1]-5)
        text_P2 = Point2(BB[0]+BB[2]+5,BB[1]-5)
        text_P3 = Point2(BB[0]+BB[2]+5,BB[1]+BB[3]+5)
        text_P4 = Point2(BB[0]-5,BB[1]+BB[3]+5)

        line = Line2(text_P1,text_P3)
        up1 = Cognition.GetUParam(text_P1,line) 
        up2 = Cognition.GetUParam(text_P3,line)
        if up2 > up1:
            Rect1_p1 = text_P1
            Rect1_p2 = text_P3            
        else:
            Rect1_p1 = text_P3
            Rect1_p2 = text_P1
        Rect1_p3 = text_P2
        Rect1_p4 = text_P4
        OrientationAngle = 0
        for i in Dimensionallines:
            for l in i._Leaders:
                line = l
                P1 = l.startPoint
                P2 = l.endPoint
                Rect2_p1 = Point2(P1.x-6, P1.y-6)
                Rect2_p2 = Point2(P2.x+6, P2.y+6)
                Rect2_p3 = Point2(P2.x+6,P2.y-6)
                Rect2_p4 = Point2(P1.x-6,P1.y+6)
                Rect1_Segments = [Line2(Rect1_p1, Rect1_p2), Line2(Rect1_p2, Rect1_p3), Line2(Rect1_p3, Rect1_p4), Line2(Rect1_p4, Rect1_p1)]
                Rect2_Segments = [Line2(Rect2_p1, Rect2_p2), Line2(Rect2_p2, Rect2_p3), Line2(Rect2_p3, Rect2_p4), Line2(Rect2_p4, Rect2_p1)]
                overlap = Cognition.CheckIfOverlapLineSegments(Rect1_Segments, Rect2_Segments)
                if overlap == True:
                    OrientationAngle = Cognition.getAngleBetweenLineAndAxis(P1,P2)
                    return OrientationAngle
        return OrientationAngle

    @staticmethod
    def MidPoint(p1, p2):
        return Point2(int((p1.x + p2.x)/2), int((p1.y + p2.y)/2))

    @staticmethod
    def DimensionProximityCorrelation(Detection_Manager):
        DimensionCorrelated = []
        Dimensionallines = Detection_Manager._DetectedDimensionalLine
        DimensionalText = Detection_Manager._DetectedDimensionalText  
        for DT in DimensionalText:
            
            text_P1 = Point2(DT._TextBoxP1.x - 3, DT._TextBoxP1.y - 3)
            text_P2 = Point2(DT._TextBoxP2.x + 3, DT._TextBoxP1.y - 3)
            text_P3 = Point2(DT._TextBoxP2.x + 3, DT._TextBoxP2.y + 3)
            text_P4 = Point2(DT._TextBoxP1.x - 3, DT._TextBoxP2.y + 3)
    
            line = Line2(text_P1,text_P3)
            up1 = Cognition.GetUParam(text_P1,line) 
            up2 = Cognition.GetUParam(text_P3,line)
            if up2 > up1:
                Rect1_p1 = text_P1
                Rect1_p2 = text_P3            
            else:
                Rect1_p1 = text_P3
                Rect1_p2 = text_P1
            Rect1_p3 = text_P2
            Rect1_p4 = text_P4
            overlap = False
            for i in Dimensionallines:
                if overlap != True:
                    for l in i._Leaders:
                        line = l
                        up1 = Cognition.GetUParam(l.startPoint,line)
                        up2 = Cognition.GetUParam(l.endPoint,line)
                        if up2 > up1:
                            P1 = l.startPoint
                            P2 = l.endPoint 
                        else:
                            P1 = l.endPoint
                            P2 = l.startPoint
                        Rect2_p1 = Point2(P1.x-6, P1.y-6)
                        Rect2_p2 = Point2(P2.x+6, P2.y+6)
                        Rect2_p3 = Point2(P2.x+6,P2.y-6)
                        Rect2_p4 = Point2(P1.x-6,P1.y+6)
                        Rect1_Segments = [Line2(Rect1_p1, Rect1_p2), Line2(Rect1_p2, Rect1_p3), Line2(Rect1_p3, Rect1_p4), Line2(Rect1_p4, Rect1_p1)]
                        Rect2_Segments = [Line2(Rect2_p1, Rect2_p2), Line2(Rect2_p2, Rect2_p3), Line2(Rect2_p3, Rect2_p4), Line2(Rect2_p4, Rect2_p1)]
                        overlap = Cognition.CheckIfOverlapLineSegments(Rect1_Segments, Rect2_Segments)
                        if overlap == True:
                            D = Dimensions()
                            D.ExtractDimension(D, i, DT)
                            DimensionCorrelated.append(D)
                            break
                else:
                    break
                        
        return DimensionCorrelated

    @staticmethod
    def SortCoordinates(points):
        Pts = {}
        for i in points:
            val = ((i.x) * 1000) + (i.y)
            Pts[val] = i
        keys = Pts.keys()
        sortedKeys = sorted(keys)
        sortedPts = []
        for i in range(0, len(sortedKeys)):
          key = sortedKeys[i]
          point = Pts[key]
          sortedPts.append(point)
        return sortedPts

    @staticmethod
    def ProximityCorrelation(Detection_Manager):
        TextBoxes = Detection_Manager._DetectedDimensionalText
        DimensionalLines = Detection_Manager._DetectedDimensionalLine
        TextBox_Midpoints = {}
        TextBox_Midpointslist = []
        for i in TextBoxes:
            md_point = Cognition.MidPoint(i._TextBoxP1, i._TextBoxP2)
            TextBox_Midpoints[md_point] = i
            TextBox_Midpointslist.append(md_point)
        sortedTextBoxMidpoints = Cognition.SortCoordinates(TextBox_Midpointslist)
        sortedTextBoxPoints = []
        for i in sortedTextBoxMidpoints:
            for j in TextBox_Midpoints.keys():
                if int(i.x) == int(j.x) and int(i.y) == int(j.y):
                    val = TextBox_Midpoints[j]
                    sortedTextBoxPoints.append(val)

        DimensionalLine_Midpoints = {}
        DimensionalLine_Midpointslist = []
        for DL in DimensionalLines:
            for i in DL._Leaders:
                P1 = Point2(i.startPoint.x - 6, i.startPoint.y - 6)
                P2 = Point2(i.endPoint.x + 6, i.endPoint.y + 6)
                md_point = Cognition.MidPoint(P1, P2)
                DimensionalLine_Midpoints[md_point] = DL
                DimensionalLine_Midpointslist.append(md_point)
        sortedLineMidpoints = Cognition.SortCoordinates(DimensionalLine_Midpointslist)
        sortedLinePoints = []
        for i in sortedLineMidpoints:
            for j in DimensionalLine_Midpoints.keys():
                if int(i.x) == int(j.x) and int(i.y) == int(j.y):
                    val = DimensionalLine_Midpoints[j]
                    sortedLinePoints.append(val)
        DimensionCorrelated = []
        removedLs = []
        for i in sortedTextBoxPoints:
            text_P1 = Point2(i._TextBoxP1.x - 3, i._TextBoxP1.y - 3)
            text_P2 = Point2(i._TextBoxP2.x + 3, i._TextBoxP1.y - 3)
            text_P3 = Point2(i._TextBoxP2.x + 3, i._TextBoxP2.y + 3)
            text_P4 = Point2(i._TextBoxP1.x - 3, i._TextBoxP2.y + 3)
            line = Line2(text_P1,text_P3)
            up1 = Cognition.GetUParam(text_P1,line) 
            up2 = Cognition.GetUParam(text_P3,line)
            if up2 > up1:
                Rect1_p1 = text_P1
                Rect1_p2 = text_P3            
            else:
                Rect1_p1 = text_P3
                Rect1_p2 = text_P1
            Rect1_p3 = text_P2
            Rect1_p4 = text_P4
            
            overlap = False
            for j in sortedLinePoints:
                if overlap != True:
                    if j not in removedLs:
                        for l in j._Leaders:
                            line = l
                            P1 = l.startPoint
                            P2 = l.endPoint
                            Rect2_p1 = Point2(P1.x-6, P1.y-6)
                            Rect2_p2 = Point2(P2.x+6, P2.y+6)
                            Rect2_p3 = Point2(P2.x+6,P2.y-6)
                            Rect2_p4 = Point2(P1.x-6,P1.y+6)
                            Rect1_Segments = [Line2(Rect1_p1, Rect1_p2), Line2(Rect1_p2, Rect1_p3), Line2(Rect1_p3, Rect1_p4), Line2(Rect1_p4, Rect1_p1)]
                            Rect2_Segments = [Line2(Rect2_p1, Rect2_p2), Line2(Rect2_p2, Rect2_p3), Line2(Rect2_p3, Rect2_p4), Line2(Rect2_p4, Rect2_p1)]
                            overlap = Cognition.CheckIfOverlapLineSegments(Rect1_Segments, Rect2_Segments)
                            if overlap == True:
                                removedLs.append(j)
                                D = Dimensions()
                                D.ExtractDimension(D, j, i)
                                DimensionCorrelated.append(D)
                                break
                else:
                    break
                        
        return DimensionCorrelated

    @staticmethod
    def AssignArrowHeadsDirection(ArrowHeadsList, center, Direction):
        for a in ArrowHeadsList:
            arrow_center = a._ArrowCenter
            if fabs(int(arrow_center.x - center.x)) <= 3 and fabs(int(arrow_center.y - center.y)) <= 3:
                a._Direction = Direction
                return

    @staticmethod
    def GetDirection(p, c):
        if fabs(p.x - c.x) < 10:
            if p.y < c.y+10:
                return "North"
            elif p.y > c.y+10:
                return "South"
        elif p.x < c.x+10 :
            if fabs(p.y - c.y) < 10:
                return "West"
            elif p.y < c.y+10:
                return "NorthWest"
            elif p.y > c.y+10:
                return "SouthWest"
        elif p.x > c.x+10:
            if fabs(p.y - c.y) < 10:
                return "East"
            elif p.y < c.y+10:
                return "NorthEast"
            elif p.y > c.y+10:
                return "SouthEast"

    @staticmethod
    def ArrowHeadDirection(Feature_Manager):
        OriginalImg = Feature_Manager._ImageOriginal.copy()
        OutputImg = OriginalImg.copy()
        DimensionalLines = Feature_Manager._DetectedDimensionalLine
        ArrowHeadsList = Feature_Manager._DetectedArrowHead
        for dl in DimensionalLines:
            for ah in dl._ArrowHeads:
                p1 = ah._BoundingBoxP1
                p2 = ah._BoundingBoxP2
                TempImg = OriginalImg[p1.y:p2.y+4, p1.x:p2.x+4]
                TempImg = ImgTransform.ImgAspectResize(TempImg, 100, 100)
                
                cornerImg = TempImg.copy()
                gray = cv2.cvtColor(TempImg,cv2.COLOR_BGR2GRAY)
                corners = cv2.goodFeaturesToTrack(gray,20,0.09,10, True)
                corners = np.int0(corners)
                cornerPts = []
                xpts = []
                ypts = []
                for i in corners:
                    x,y = i.ravel()
                    p = Point2(x,y)
                    xpts.append(x)
                    ypts.append(y)
                    cornerPts.append(p)
                    cv2.circle(cornerImg,(x,y),1,255,-1)
                xc = np.mean(xpts)
                yc = np.mean(ypts)
                c = Point2(xc,yc)
                dictPt = {}
                for i in cornerPts:
                    d = sqrt((c.x - i.x)**2 + (c.y - i.y)**2)
                    dictPt[i] = d
                sortedDict = sorted(dictPt.items(), key= operator.itemgetter(1))
                extremePt = sortedDict[len(sortedDict) - 1][0]
                cv2.circle(cornerImg,(extremePt.x,extremePt.y),3,255,-1)
                projectedPt = MathUtils.ProjectToLine2(dl._Leaders[0].startPoint, dl._Leaders[0].endPoint, extremePt)
                projectedCorner = MathUtils.ProjectToLine2(dl._Leaders[0].startPoint, dl._Leaders[0].endPoint, c)
                Direction = Cognition.GetDirection(projectedPt, projectedCorner)
                ah._Direction = Direction
                Cognition.AssignArrowHeadsDirection(ArrowHeadsList, ah._ArrowCenter, Direction)
                print(Direction)

    @staticmethod
    def CheckThicknessInVicinity(x, y, distImg):
        scanRange = 3
        thickness = []
        imgHeight, imgWidth = distImg.shape
        if x < (imgWidth - scanRange) and y < (imgHeight - scanRange):
            for i in range(-scanRange, scanRange):
               for j in range(-scanRange, scanRange):
                  xj = int(x + j)
                  yi = int(y + i)
                  t = distImg[yi][xj]
                  thickness.append(t)
            t = max(thickness)
            scanRange = [-2,-1, 0, 1, 2] 
            if t <= 1.5:
                t = 0
                for i in scanRange:
                    for j in scanRange:
                        xj = int(x + j)
                        yi = int(y + i)
                        thick = distImg[yi][xj]
                        if round(thick) == 1:
                            t += 1
                if t > 5:
                    return 2
                else:
                    return 1
            else:
                return (t+1)
        
    @staticmethod
    def Thickness(point1, point2, img):
        p1 =Point2(point1.x-2, point1.y-2)
        p2 =Point2(point2.x+2, point2.y+2)
        Image = img[p1.y:p2.y, p1.x:p2.x]
        gray = cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        dist_img = cv2.distanceTransform(thresh,cv2.DIST_L2,5)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(dist_img)
        return maxVal
        
    @staticmethod
    def DistanceTransform(img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        dist_img = cv2.distanceTransform(thresh,cv2.DIST_L2,5)
        return dist_img

    @staticmethod
    def MergeLineSegments(uniqueLines):
        UQLines = []
        for l in uniqueLines:
            lines = []
            if len(l) > 1:
                for id in range(0,len(l)-1):
                    LS1 = l[id]
                    LS2 = l[id + 1]
                    d = LS2.startPoint.DistanceTo(LS1.endPoint)
                    newLS = l[id + 1]
                    if d <= 5:
                        newLS = Line2(LS1.startPoint, LS2.endPoint)
                        l[id+1] = newLS
                    else:
                        lines.append(l[id])
                lines.append(newLS)
            elif len(l) == 1:
                lines.append(l[0])
            else:
                continue
            if len(lines) !=0 :
                UQLines.append(lines)
        return UQLines
 
    @staticmethod
    def CheckNearbySegments(segment, EntityLines):
        s = segment.startPoint
        e = segment.endPoint
        newStartPoint = s
        newEndPoint = e
        for l in EntityLines:
            for ls in l:
                if 5 >= fabs(s.x - ls.startPoint.x) > 0 and 5 >= fabs(s.y - ls.startPoint.y) > 0:
                    A1, B1, C1 = Cognition.LineCoefficients(s, e)
                    A2, B2, C2 = Cognition.LineCoefficients(ls.startPoint, ls.endPoint)
                    det = A1*B2 - A2*B1
                    if (det != 0):
                        x = (B2*C1 - B1*C2)/det
                        y = (A1*C2 - A2*C1)/det
                        IntersectionPt = Point2(x,y)
                        newStartPoint = IntersectionPt
                elif 5 >= fabs(s.x - ls.endPoint.x) > 0 and 5 >= fabs(s.y - ls.endPoint.y) > 0:
                    A1, B1, C1 = Cognition.LineCoefficients(s, e)
                    A2, B2, C2 = Cognition.LineCoefficients(ls.startPoint, ls.endPoint)
                    det = A1*B2 - A2*B1
                    if (det != 0):
                        x = (B2*C1 - B1*C2)/det
                        y = (A1*C2 - A2*C1)/det
                        IntersectionPt = Point2(x,y)
                        newStartPoint = IntersectionPt
                   
        for l in EntityLines:
            for ls in l:                        
                if 5 >= fabs(e.x - ls.endPoint.x) > 0 and 5 >= fabs(e.y - ls.endPoint.y) > 0:
                    A1, B1, C1 = Cognition.LineCoefficients(s, e)
                    A2, B2, C2 = Cognition.LineCoefficients(ls.startPoint, ls.endPoint)
                    det = A1*B2 - A2*B1
                    if (det != 0):
                        x = (B2*C1 - B1*C2)/det
                        y = (A1*C2 - A2*C1)/det
                        IntersectionPt = Point2(x,y)
                        newEndPoint = IntersectionPt
                elif 5 >= fabs(e.x - ls.startPoint.x) > 0 and 5 >= fabs(e.y - ls.startPoint.y) > 0:
                    A1, B1, C1 = Cognition.LineCoefficients(s, e)
                    A2, B2, C2 = Cognition.LineCoefficients(ls.startPoint, ls.endPoint)
                    det = A1*B2 - A2*B1
                    if (det != 0):
                        x = (B2*C1 - B1*C2)/det
                        y = (A1*C2 - A2*C1)/det
                        IntersectionPt = Point2(x,y)
                        newEndPoint = IntersectionPt
        newSegment = Line2(newStartPoint, newEndPoint)
        return newSegment            

    @staticmethod
    def CorrectEnds(Detection_Manager):
        entityline = Detection_Manager._DetectedLine
        eLines = []
        for l in entityline:
            elinesegments = []
            for ls in l:
                segment = Cognition.CheckNearbySegments(ls, entityline)
                SegmentLength = segment.Length()
                if SegmentLength > 6:
                    elinesegments.append(segment)
            if len(elinesegments) > 0:
                eLines.append(elinesegments)

        Detection_Manager._DetectedLine = eLines

    @staticmethod
    def flattenLineSegmentLists(lineSegments):
        flattened = []
        for lsList in lineSegments:
            for ls in lsList: 
                flattened.append(ls)
        return flattened

    @staticmethod
    def areSameLineSegments(lsa, lsb):
        if ((lsa.startPoint == lsb.startPoint) and (lsa.endPoint == lsb.endPoint)) or ((lsa.startPoint == lsb.endPoint) and (lsa.endPoint == lsb.startPoint)):
            return True

    @staticmethod
    def GetNearestLineSegment(point, ls, lineSegments):
        if lineSegments.Length == 0:
            return None
        nearestSegment = None
        minDist = sys.float_info.max
        nearestPoint = None
        for l in lineSegments:
            if Cognition.areSameLineSegments(l, ls):
                continue
            nearestPointDist, nearestPoint = MathUtils.MinDistance_PointToLineSegment(l.startPoint, l.endPoint, point)
            if minDist >= nearestPointDist:
                nearestSegment = l
                minDist = nearestPointDist
                nearestPoint = nearestPoint
        return nearestSegment, minDist, nearestPoint

    @staticmethod
    def JoinLineSegmentsWithinProximityTolerance(Feature_Manager):
        entityLineSegments =  Feature_Manager._DetectedLine
        PIXEL_TOLERANCE = 8         
        updatedLineSegments = []
        lineSegments = Cognition.flattenLineSegmentLists(entityLineSegments)

        for lsToExtend in lineSegments:
            dir = lsToExtend.endPoint - lsToExtend.startPoint
            dir = dir.Normalize()
            start = lsToExtend.startPoint + (dir.Negate() * PIXEL_TOLERANCE)
            end = lsToExtend.endPoint + (dir * PIXEL_TOLERANCE)

            minDistanceStart = sys.float_info.max
            minDistanceEnd = sys.float_info.max
            startExtensionPoint = None
            endExtensionPoint = None

            for lsTemp in lineSegments:
                if lsTemp == lsToExtend:
                    continue

                result, intersection = MathUtils.Intersects_LineSegmentLineSegment(lsTemp.startPoint, lsTemp.endPoint, start, end)
                if result == False or intersection is None:
                    continue

                dist = lsToExtend.startPoint.DistanceTo(intersection)
                if dist < minDistanceStart and dist < PIXEL_TOLERANCE:
                     minDistanceStart = dist
                     startExtensionPoint = intersection

                dist = lsToExtend.endPoint.DistanceTo(intersection)
                if dist < minDistanceEnd and dist < PIXEL_TOLERANCE:
                     minDistanceEnd = dist
                     endExtensionPoint = intersection

            if startExtensionPoint is not None and minDistanceStart <= PIXEL_TOLERANCE:
                lsToExtend.startPoint = startExtensionPoint

            if endExtensionPoint is not None and minDistanceEnd <= PIXEL_TOLERANCE:
                lsToExtend.endPoint = endExtensionPoint

            updatedLineSegments.append(lsToExtend)

        Feature_Manager._DetectedLine = updatedLineSegments

    @staticmethod
    def EntityCorrelation(Feature_Manager):
        entityLines = Feature_Manager._DetectedLine
        dimensions = Feature_Manager._DetectedDimension
        EntitiesCorrelated = []
        for d in dimensions:
            CorrelatedLines = []
            cE = CorrelatedEntity()
            for a in d._DimensionalLines._ArrowHeads:
                BB = Cognition.SortCoordinates([a._BoundingBoxP1, a._BoundingBoxP2])
                bbMin = BB[0]
                bbMax = BB[1]
                direction = a._Direction
                if direction == "West":
                    shortListedLines = []
                    for l in entityLines:
                        if bbMin.x + 3 > l.startPoint.x and fabs(l.endPoint.x - l.startPoint.x) < 3 and fabs(l.endPoint.y - l.startPoint.y) > 5 :
                                shortListedLines.append(l)                                
                               
                    for l in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(l.startPoint, l.endPoint, bbMin)
                            projectedDistance = bbMin.DistanceTo(projectedPt)
                            if projectedDistance < 8 :          #<7
                                CorrelatedLines.append(l)
                                
                elif direction == "East":
                   shortListedLines = []
                   for l in entityLines:
                       
                           if bbMax.x - 3 < l.startPoint.x and fabs(l.endPoint.x - l.startPoint.x) < 3 and fabs(l.endPoint.y - l.startPoint.y) > 5:
                               shortListedLines.append(l)
                               
                   for l in shortListedLines:
                       
                           projectedPt = MathUtils.ProjectToLine2(l.startPoint, l.endPoint, bbMax)
                           projectedDistance = bbMax.DistanceTo(projectedPt)
                           if projectedDistance < 8 :       #<7
                               CorrelatedLines.append(l)
                               
                elif direction == "North":
                    shortListedLines = []
                    for l in entityLines:
                            if bbMin.y + 3 > l.startPoint.y and fabs(l.endPoint.y - l.startPoint.y) < 3 and fabs(l.endPoint.x - l.startPoint.x) > 5:
                                shortListedLines.append(l)
                                
                    for l in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(l.startPoint, l.endPoint, bbMin)
                            projectedDistance = bbMin.DistanceTo(projectedPt)
                            if projectedDistance < 8 :      #<7
                                CorrelatedLines.append(l)
                                
                elif direction == "South":
                    shortListedLines = []
                    for l in entityLines:
                            if bbMax.y - 3 < l.startPoint.y and fabs(l.endPoint.y - l.startPoint.y) < 3 and fabs(l.endPoint.x - l.startPoint.x) > 5:
                                shortListedLines.append(l)
                                
                    for l in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(l.startPoint, l.endPoint, bbMax)
                            projectedDistance = bbMax.DistanceTo(projectedPt)
                            if projectedDistance < 8 :      #<7
                                CorrelatedLines.append(l)
                                
            cE.ExtractCorrelatedEntity(cE, d, CorrelatedLines)
            EntitiesCorrelated.append(cE)
        Feature_Manager._CorrelatedEntities = EntitiesCorrelated
                                  


        


    



