# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from math import fabs, sqrt
from Core.Math.Point2 import Point2
from Core.Math.Vector3 import Vector3
from Core.Math.Constants import Constants

class Point3:

    def __init__ (self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __init__(self , x_init , y_init , z_init ):
        self.x = x_init
        self.y = y_init
        self.z = z_init

    def __eq__(self, other):
        tol = Constants.PRECISION
        return ( fabs(self.x - other.x) < tol and fabs(self.y - other.y) < tol and fabs(self.z - other.z) < tol)
    
    def __repr__(self):
        return "".join(["Point3(", str(self.x), ",", str(self.y),",", str(self.z), ")"])

    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __sub__ (self, other):
        return Vector3(self.x - other.x , self.y - other.y, self.z - other.z)

    def __add__ (self, other):
        return Point3(self.x + other.i, self.y + other.j, self.z + other.k)

    def __mul__ (self, scalar):
        return Point3((self.x * scalar),(self.y * scalar), (self.z * scalar))

    def DistanceTo(self, other):
        d = sqrt(((self.x - other.x) * (self.x - other.x)) + ((self.y - other.y) * (self.y - other.y)) + ((self.z - other.z) * (self.z - other.z)))
        return d

    @staticmethod    
    def Centroid(Points):
        
        totalX = 0
        totalY = 0
        totalZ = 0
        for i in Points:
            totalX += i.x
            totalY += i.y
            totalZ += i.z
        return Point3(totalX/(len(Points)), totalY/(len(Points)), totalZ/(len(Points)))

    @staticmethod
    def CalculateNormal (first, second, third):
        v1 = Vector3( second.x - first.x, second.y - first.y, second.z - first.z)
        v2 = Vector3( third.x - second.x, third.y - second.y, third.z - second.z)
        normal = v1.Cross(v2)
        normal.Normalize()
        return normal

    @staticmethod
    def AreCollinear(first, second, third):
        if (first == second or first == third or second == third):
            return True
        
        v1 = Vector3(first.x - second.x, first.y - second.y, first.z - second.z)
        v2 = Vector3(first.x - third.x, first.y - third.y, first.z - third.z)
        angle = Vector3.AngleDeg(v1,v2)
       
        if ((fabs(angle) < Constants.PRECISION) or (fabs(angle - 180) < Constants.PRECISION)):
            return True
        return False
    
    def ToPoint2(self):
        return Point2(self.x , self.y)

    @staticmethod
    def Project(point, planePt, planeNorm):
        planeNormal = planeNorm.Normalize()
        v = point - planePt
        dot = v.Dot(planeNormal)
        dv = planeNormal * dot
        return Point3(point.x - dv.i, point.y - dv.j, point.z - dv.k)


