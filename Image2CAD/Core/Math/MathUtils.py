# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from Core.Math.Point2 import Point2
from Core.Math.Point3 import Point3
from Core.Math.Vector2 import Vector2
from Core.Math.Vector3 import Vector3
from Core.Math.Constants import Constants
from math import sqrt, acos, fabs

class MathUtils:

    @staticmethod
    def EQTF(a, b, tol):
        tol = Constants.PRECISION
        return (fabs(a - b) < tol)

    @staticmethod
    def  RadToDeg(angle):
        return (57.2957795130823208768 * angle)

    @staticmethod
    def DegToRad(angle):
        return (0.01745329251994329577 * angle)
    
    @staticmethod
    def IsInTriangle(p, a, b, c):
       inside = True
       v1 = b - a
       v2 = c - a
       v3 = p - a
       normal = v1.Cross(v2)
       tempVec = v1.Cross(v3)

       if ( tempVec.Dot(normal) < 0):
            inside = False
       else:
            tempVec = (c - a).Cross(p - b)
            if ( tempVec.Dot(normal) < 0):
                inside = False
            else:
                tempVec = (a - c).Cross(p - c)
                if ( tempVec.Dot(normal) < 0):
                    inside = False
       return inside


    @staticmethod
    def ProjectToPlane(point, planeNormal, planePoint):
        normal = planeNormal
        normal.Normalize()
        v1 = point - planePoint
        distance = v1.Dot(normal)
        return Point3((point.x - (normal.i * distance)), (point.y - (normal.j * distance)), (point.z - (normal.k * distance)))


    @staticmethod
    def CalculateInnerAngleDeg( pointBefore, basePoint, pointAfter):
        v1 = pointBefore - basePoint
        v2 = pointAfter - basePoint
        nomvec = Point3.CalculateNormal(pointBefore, basePoint, pointAfter)
        normal = nomvec
        angle = v1.AngleDeg(v1, v2)

        if (normal.k > 0):
            angle = 360 - angle
        return angle


    @staticmethod
    def ProjectToLineDirection( point, lineDirection, linePoint):
        id = lineDirection
        id.Normalize()

        anotherPointOnLine = (linePoint + (id * 100.0))
        v = (anotherPointOnLine - linePoint)
        denominator = v.Dot(v)
        if ( fabs(denominator) < Constants.PRECISION):
            return linePoint

        vec1 = (point - linePoint)
        vec2 = (anotherPointOnLine - linePoint)

        u = (vec1.Dot(vec2)) / denominator
        return (linePoint + (v * u))


    @staticmethod
    def ProjectToLine( p1, p2, p):
        v1 = (p2 - p1)
        denominator = v1.Dot(v1)
        if (fabs(denominator) < Constants.PRECISION):
            return p1
        v2 = (p - p1)
        u = (v1.Dot(v2)) / denominator
        x = p1.x + (u * (p2.x - p1.x))
        y = p1.y + (u * (p2.y - p1.y))
        z = p1.z + (u * (p2.z - p1.z))

        return Point3(x, y, z)

    @staticmethod
    def ProjectToLine2( p1, p2, p):
        v1 = (p2 - p1)
        denominator = v1.Dot(v1)

        if (fabs(denominator) < Constants.PRECISION):
            return p1

        v2 = (p - p1)
        u = (v1.Dot(v2)) / denominator
        x = p1.x + (u * (p2.x - p1.x))
        y = p1.y + (u * (p2.y - p1.y))

        return Point2(x, y)


    @staticmethod
    def Distance_PointToPlane(point, planePoint, planeNormal):
        normal = planeNormal.Normalize()
        v = (point - planePoint)
        return fabs(v.Dot(normal))


    @staticmethod
    def DistanceSigned_PointToPlane(point, planePoint, planeNormal):
        normal = planeNormal.Normalize()
        v = (point - planePoint)
        return (v.Dot(normal))


    @staticmethod
    def Distance_PointToLine(lineStart, dir, point):
        direction = dir.Normalize()
        lineEnd = lineStart + (direction * 100.0)
        projection = MathUtils.ProjectToLine(lineStart, lineEnd, point)
        return point.DistanceTo(projection)

    @staticmethod
    def Distance_PointToLine2(lineStart, dir, point):
        direction = dir.Normalize()
        lineEnd = lineStart + (direction * 100.0)
        projection = MathUtils.ProjectToLine2(lineStart, lineEnd, point)
        return point.DistanceTo(projection)

    @staticmethod
    def Distance_PointToLinePoint(lineStart, lineEnd, point):
        dir = lineEnd - lineStart
        direction = dir.Normalize()
        lineEnd = lineStart + (direction * 100.0)
        projection = MathUtils.ProjectToLine2(lineStart, lineEnd, point)
        return point.DistanceTo(projection)

    @staticmethod
    def MinDistance_PointToLineSegment(lineStart, lineEnd, point):
        projection = MathUtils.ProjectToLine2(lineStart, lineEnd, point)
        d1 = lineStart.DistanceTo(point)
        d2 = lineEnd.DistanceTo(point)
        dp = projection.DistanceTo(point)
        minDist = d1
        nearestPoint = lineStart
        if d2 < minDist:
            minDist = d2
            nearestPoint = lineEnd
        if dp < minDist:
            minDist = dp
            nearestPoint = projection
        return minDist, nearestPoint

    @staticmethod
    def areSame(a, b):
        return ((a <= b + Constants.PRECISION) and (a >= b - Constants.PRECISION))

    @staticmethod
    def areSame(v1, v2):
        return (MathUtils.areSame(v1.i, v2.i) and MathUtils.areSame(v1.j, v2.j) and MathUtils.areSame(v1.k, v2.k))

    @staticmethod
    def CheckForCoincidentLineSegments( p1, p2, p3, p4):
        tolerance = Constants.PRECISION
        if (MathUtils.Distance_PointToLinePoint(p3, p2, p1) < tolerance):
            return True
        if (MathUtils.Distance_PointToLinePoint(p4, p2, p1) < tolerance):
            return True
        if (MathUtils.Distance_PointToLinePoint(p1, p4, p3) < tolerance):
            return True
        if (MathUtils.Distance_PointToLinePoint(p2, p4, p3) < tolerance):
            return True
        return False
    

    @staticmethod
    def Check_Intersects_LineSegmentLineSegment(p1, p2, p3, p4):
        tolerance = Constants.PRECISION
        Pixeltolerance =  Constants.PIXEL_PRECISION

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
                return MathUtils.CheckForCoincidentLineSegments(p1, p2, p3, p4)
            return False                 #False..but to check for Boundingbox touching we changed it to True.
        ua = numeratorA / denominator
        ub = numeratorB / denominator

        if((ua > (0.0 - Pixeltolerance)) and (ua < (1.0 + Pixeltolerance)) and (ub > (0.0 - Pixeltolerance)) and (ub < (1.0 + Pixeltolerance))):
            intersection = p1 + (p2 -p1) * ua
            return True
        return False

    @staticmethod
    def Intersects_LineSegmentLineSegment(p1, p2, p3, p4):
        tolerance = Constants.PRECISION

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
                areCoincident = MathUtils.CheckForCoincidentLineSegments(p1, p2, p3, p4)
                return areCoincident, None
            return False, None

        ua = numeratorA / denominator
        ub = numeratorB / denominator

        if((ua > (0.0 - tolerance)) and (ua < (1.0 + tolerance)) and (ub > (0.0 - tolerance)) and (ub < (1.0 + tolerance))):
            intersection = p1 + (p2 -p1) * ua
            return True, intersection

        return False, None


    