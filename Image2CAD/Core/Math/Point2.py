# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from math import fabs, sqrt
#from Core.Math.Point3 import Point3
from Core.Math.Vector2 import Vector2
from Core.Math.Vector3 import Vector3
from Core.Math.Constants import Constants

class Point2:

    def __init__(self):
        self.x = 0
        self.y = 0   
    
    def __init__(self, other):
        self.x = other.x
        self.y = other.y   

    def __init__(self, x_init, y_init ):
        self.x = x_init
        self.y = y_init

    def __repr__(self):
        return "".join(["Point2(", str(self.x), ",", str(self.y), ")"])

    def __eq__(self, other):
        tol = Constants.PRECISION
        return (fabs(self.x - other.x) < tol and fabs(self.y - other.y) < tol )
    
    def __lt__(self, other):
        return (self.x < other.x and self.y < other.y )
    
    def __hash__(self):
      return hash((self.x, self.y))
  
    def __sub__ (self, other):
        return Vector2(self.x - other.x , self.y - other.y)

    
    def __add__ (self, other):
        return Point2(self.x + other.x , self.y + other.y)

    def __add__ (self, other):
        return Point2(self.x + other.i , self.y + other.j)

    def __mul__ (self, scalar):
        return Point2((self.x * scalar),(self.y * scalar))
        

    def DistanceTo(self, other):
        d= sqrt(((self.x - other.x) * (self.x - other.x)) + ((self.y - other.y) * (self.y - other.y)))
        return d

    @staticmethod
    def Centroid(points):
        totalX = 0
        totalY =0
        for i in points:
            totalX += i.x
            totalY += i.y
        return Point2(totalX/(len(points)),totalY/(len(points)))

    @staticmethod
    def CalculateNormal (first, second, third):
        v1 = Vector3.Vector3( second.x - first.x, second.y - first.y, 0)
        normal = Vector3.Vector3(v1.y, -v1.x, 0)
        normal.Normalize()
        return print('Normal Vector', normal)

    @staticmethod
    def AreCollinear(first, second, third):
        if (first == second or first == third or second == third):
            return True
        v1 = Vector3(first.x - second.x, first.y - second.y, 0)
        v2 = Vector3(first.x - third.x, first.y - third.y, 0)
        angle = Vector3.AngleDeg(v1,v2)
        if ((fabs(angle) < Constants.PRECISION) or (fabs(angle - 180) < Constants.PRECISION)):
            return True
        return False

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

        return Point2(x, y)

    @staticmethod
    def ProjectToLineDirection( point, point1Line, point2Line, linePoint):
        id = point2Line - point1Line
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


    
    
        

    


        
    

