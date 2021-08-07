# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
from math import fabs
from Core.Math.Point2 import Point2
from Core.Math.Line2 import Line2
from Core.Math.MathUtils import MathUtils
from Core.Features.Cognition.Cognition import Cognition
from Core.Features.LineSegments.SpecialLineSegments import SpecialLineSegments

class SupportLinesFeature():

    @staticmethod
    def Detect(Feature_Manager):
        
        lines = Feature_Manager._DetectedLine
        dimension = Feature_Manager._DetectedDimension
        supportLinesegments = []
        entityLinesegments = []
        dist_Img = Cognition.DistanceTransform(Feature_Manager._ImageCleaned)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(dist_Img)
        for l in lines:
            for seg in l:
                PointsBetweenLine = SpecialLineSegments.PixelScanner(seg.startPoint,seg.endPoint,dist_Img)
                sLinesPoints = []
                eLinePoints = []
                for i in PointsBetweenLine:
                    t = Cognition.CheckThicknessInVicinity(i[0],i[1], dist_Img)
                    pt = Point2(i[0],i[1])
                    if t is None:
                        continue
                    if t <= 0.6 * maxVal:           
                        sLinesPoints.append(pt)
                    else:
                        eLinePoints.append(pt)
                sortSuppPts = sLinesPoints
                sortEntPts = eLinePoints
                if (len(sortSuppPts) > 1):
                    startsupportPt = sortSuppPts[0]
                    for i in range(0,len(sortSuppPts) - 1):
                        p1 = sortSuppPts[i]
                        p2 = sortSuppPts[i+1]
                        dist = p1.DistanceTo(p2)
                        if dist > 30:
                            Supportlinesegment = Line2(startsupportPt,p1)
                            supportLinesegments.append(Supportlinesegment)
                            startsupportPt = p2
                    Supportlinesegment = Line2(startsupportPt,p2)
                    supportLinesegments.append(Supportlinesegment)
                if (len(sortEntPts)> 1):
                    startentityPt = sortEntPts[0]
                    elines = []
                    for i in range(0,len(sortEntPts) - 1):
                        eline = []
                        p1 = sortEntPts[i]
                        p2 = sortEntPts[i+1]
                        dist = p1.DistanceTo(p2)
                        if dist > 2:         
                            entitylinesegment = Line2(startentityPt,p1)
                            eline.append(entitylinesegment)
                            entityLinesegments.append(eline)
                            startentityPt = p2
                    entitylinesegment = Line2(startentityPt,p2)
                    elines.append(entitylinesegment)
                    entityLinesegments.append(elines)
        for d in dimension:
            SupportL = []
            for a in d._DimensionalLines._ArrowHeads:
                BB = Cognition.SortCoordinates([a._BoundingBoxP1, a._BoundingBoxP2])
                bbMin = BB[0]
                bbMax = BB[1]
                direction = a._Direction
                if direction == "West":
                    shortListedLines = []
                    SupportLSW = []
                    for ls in supportLinesegments: 
                            if bbMin.x + 3 > ls.startPoint.x and fabs(ls.endPoint.x - ls.startPoint.x) < 3 and fabs(ls.endPoint.y - ls.startPoint.y) > 5 :
                                shortListedLines.append(ls)   
                    for ls in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(ls.startPoint, ls.endPoint, bbMin)
                            projectedDistance = bbMin.DistanceTo(projectedPt)
                            if projectedDistance < 8 :          #<7
                                SupportLSW.append(ls)
                    SupportL.append(SupportLSW)
                elif direction == "East":
                   shortListedLines = []
                   SupportLSE = []
                   for ls in supportLinesegments: 
                           if bbMax.x - 3 < ls.startPoint.x and fabs(ls.endPoint.x - ls.startPoint.x) < 3 and fabs(ls.endPoint.y - ls.startPoint.y) > 5:
                               shortListedLines.append(ls)
                   for ls in shortListedLines:
                           projectedPt = MathUtils.ProjectToLine2(ls.startPoint, ls.endPoint, bbMax)
                           projectedDistance = bbMax.DistanceTo(projectedPt)
                           if projectedDistance < 8 :    
                               SupportLSE.append(ls)
                   SupportL.append(SupportLSE)
                elif direction == "North":
                    shortListedLines = []
                    SupportLSN = []
                    for ls in supportLinesegments:
                            if bbMin.y + 3 > ls.startPoint.y and fabs(ls.endPoint.y - ls.startPoint.y) < 3 and fabs(ls.endPoint.x - ls.startPoint.x) > 5:
                                shortListedLines.append(ls)
                    for ls in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(ls.startPoint, ls.endPoint, bbMin)
                            projectedDistance = bbMin.DistanceTo(projectedPt)
                            if projectedDistance < 8 :     
                                SupportLSN.append(ls)
                    SupportL.append(SupportLSN)
                elif direction == "South":
                    SupportLSS = []
                    shortListedLines = []
                    for ls in supportLinesegments:
                            if bbMax.y - 3 < ls.startPoint.y and fabs(ls.endPoint.y - ls.startPoint.y) < 3 and fabs(ls.endPoint.x - ls.startPoint.x) > 5:
                                shortListedLines.append(ls)
                    for ls in shortListedLines:
                            projectedPt = MathUtils.ProjectToLine2(ls.startPoint, ls.endPoint, bbMax)
                            projectedDistance = bbMax.DistanceTo(projectedPt)
                            if projectedDistance < 8 :     
                                SupportLSS.append(ls)
                    SupportL.append(SupportLSS) 
            d._SupportLines = SupportL
        Feature_Manager._DetectedLine = entityLinesegments
