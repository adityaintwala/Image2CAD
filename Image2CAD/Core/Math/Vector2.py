# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

from math import sqrt, fabs
from Core.Math.Constants import Constants

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

    

    


        
    
       
        
