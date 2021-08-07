# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from Core.Math.Point2 import Point2
from Core.Math.Constants import Constants
from Core.Math.MathUtils import MathUtils
from math import sqrt, fabs

class Line2:
    def __init__ (self):
        self.startPoint = Point2(0, 0)
        self.endPoint = Point2(0, 0)

    def __init__(self, other):
        self.startPoint = other.startPoint
        self.endPoint = other.endPoint

    def __init__(self, point1, point2):
        if (point1.x < point2.x):
            self.startPoint = point1
            self.endPoint = point2
        elif (point1.x > point2.x):
            self.startPoint = point2
            self.endPoint = point1
        elif (point1.y < point2.y):
            self.startPoint = point1
            self.endPoint = point2
        elif (point1.y > point2.y):
            self.startPoint = point2
            self.endPoint = point1
        else:
            self.startPoint = point1
            self.endPoint = point2
        
    def __repr__(self):
        return "".join(["Line(", str(self.startPoint), ",", str(self.endPoint), ")"])

    def Direction(self):
        v = (self.endPoint - self.startPoint)
        v.Normalize()
        return v
    
    def Length(self):
        return sqrt(((self.endPoint.x - self.startPoint.x) * (self.endPoint.x - self.startPoint.x)) + ((self.endPoint.y - self.startPoint.y) * (self.endPoint.y - self.startPoint.y)))

    def IsDegenerate(self):
        s = self.startPoint
        e = self.endPoint
        v = e - s
        denominator = v.Dot(v)
        tol = 2 * Constants.PIXEL_PRECISION     
     
        if ( fabs(denominator) < tol):
            return True
        return False

    def OnLine(self, point):
        s = self.startPoint
        e = self.endPoint
        dir = e - s
        dir.Normalize()
        d = MathUtils.Distance_PointToLine2(s, dir, point)
        if(d <= 5):             
            return True
        return False
