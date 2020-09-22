# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:34:07 2020

@author: Aditya Intwala
"""


from math import sqrt, fabs
from Math.Constants import Constants

class Vector3:
    def __init__ (self):
        self.i = 0
        self.j = 0
        self.k = 0

    def __init__ (self, other):
        self.i = other.i
        self.j = other.j
        self.k = other.k
        
    def __init__ (self, first = 0.0, second = 0.0, third = 0.0):
        self.i = first
        self.j = second
        self.k = third
        
    def __eq__(self, other):
        tol = Constants.PRECISION
        return (fabs(self.i - other.i) < tol and fabs(self.j - other.j) < tol and fabs(self.k - other.k) < tol  )
    
    def __repr__(self):
        return "".join(["Vector3(", str(self.i), ",", str(self.j),",", str(self.k), ")"])

    def __hash__(self):
        return hash((self.i, self.j, self.k))

    def __mul__ (self, scalar):
        return Vector3(self.i * scalar, self.j * scalar, self.k * scalar)
    
    def Normalize(self):
        length = self.Length()
        if ( length < Constants.PRECISION):
            return
        self.i /= length
        self.j /= length
        self.k /= length
        return Vector3(self.i, self.j, self.k)

    def Length(self):
        return (sqrt((self.i * self.i) + (self.j * self.j) + (self.k * self.k)))

    def Cross(self, other):
        return Vector3(((self.j * other.k)-(self.k * other.j)),((self.k * other.i)-(self.i * other.k)), ((self.i * other.j) - (self.j * other.i)))

    def Dot(self, other):
        return ((self.i * other.i) + (self.j * other.j) + (self.k * other.k))
    
    def Negate(self):
        return Vector3(-self.i, -self.j, -self.k)

    # @staticmethod
    # def AngleRad(self,other):
    #     v1 = Vector3(self.i, self.j, self.k)
    #     v1.Normalize()

    #     v2 = Vector3(other.i, other.j, other.k)
    #     v2.Normalize()

    #     dot = v1.Dot(v2)

    #     if (dot < -1.0):
    #         dot = -1.0
    #     if (dot > 1.0):
    #         dot = 1.0
    #     angle = acos(dot)
    #     return angle

    # @staticmethod
    # def AngleDeg(self,other):
    #     angle = self.AngleRad(self,other)
    #     return Convert.Convert.RadToDeg(angle)

   

    # @staticmethod
    # def TranslateByDistance(point , distance):
    #     v = Vector3(point.x, point.y, point.z)
    #     v.Normalize()
    #     return Point3.Point3(point.x + (v.i * distance), point.y +(v.j * distance), point.z + (v.k * distance))
