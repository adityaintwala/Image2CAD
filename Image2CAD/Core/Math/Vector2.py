# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:33:55 2020

@author: Aditya Intwala
"""


from math import sqrt, fabs
from Math.Constants import Constants

class Vector2:
    def __init__ (self):
        self.i = 0
        self.j = 0

    def __init__ (self, other):
        self.i = other.i
        self.j = other.j
        

    def __init__ (self, first, second):
        self.i = first
        self.j = second
        

    def __eq__(self, other):
        tol = Constants.PRECISION
        return (fabs(self.i - other.i) < tol and fabs(self.j - other.j) < tol )   
    
    def __repr__(self):
        return "".join(["Vector2(", str(self.i), ",", str(self.j), ")"])       
    
    def __hash__(self):
        return hash((self.i, self.j))  
    
    def __mul__ (self, scalar):
        return Vector2(self.i * scalar, self.j * scalar)

    def Negate(self):
        return Vector2(-self.i, -self.j)

    def Normalize(self):
        length = self.Length()
        if ( length < Constants.PRECISION):
            return
        self.i /= length
        self.j /= length
        
        return Vector2(self.i, self.j)

    def Length(self):
        return (sqrt((self.i * self.i) + (self.j * self.j)))

    def Perpendicular(self):
        return Vector2(self.j, - self.i)

    def Dot(self, other):
        return ((self.i * other.i) + (self.j * other.j))

    # @staticmethod
    # def AngleDeg(self,other):
    #     angle = self.AngleRad(self,other)
    #     return Convert.Convert.RadToDeg(angle)

    # @staticmethod
    # def AngleRad(self,other):
    #     v1 = Vector2(self.i, self.j)
    #     v1.Normalize()

    #     v2 = Vector2(other.i, other.j)
    #     v2.Normalize()

    #     dot = v1.Dot(v2)

    #     if (dot < -1.0):
    #         dot = -1.0
    #     if (dot > 1.0):
    #         dot = 1.0
    #     angle = acos(dot)
    #     return angle

    # @staticmethod
    # def TranslateByDistance(point , distance):
    #     v = Vector2(point.x, point.y)
    #     v.Normalize()
    #     return Point2.Point2(point.x + (v.i * distance), point.y +(v.j * distance))

    


        
    
       
        
