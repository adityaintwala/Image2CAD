# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from math import sqrt, fabs
from Core.Math.Constants import Constants

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

    