# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import numpy as np
from Core.Math.Point2 import Point2
from Core.Math.Line2 import Line2
from math import fabs

class ArrowHeads():

    def __init__(self):
        self._BoundingBoxP1 = Point2(0,0)
        self._BoundingBoxP2 = Point2(0,0)
        self._ArrowCenter = Point2(0,0)
        self._Direction = ""

    def __hash__(self):
      return hash((self._BoundingBoxP1, self._BoundingBoxP2, self._ArrowCenter, self._Direction))

    def __repr__(self):
        return "".join(["ArrowHead ( P1 = ", str(self._BoundingBoxP1), ", P2 = ", str(self._BoundingBoxP2),", Center = ", str(self._ArrowCenter),", Direction = ", str(self._Direction),")"])

    @staticmethod
    def ExtractArrowHead(self,p1, p2, center):
        self._BoundingBoxP1 = p1
        self._BoundingBoxP2 = p2
        self._ArrowCenter = center

class DimensionalLines():

    def __init__(self):
        self._ArrowHeads = ArrowHeads()
        self._Leaders = Line2(Point2(0,0),Point2(2,2))

    def __hash__(self):
      return hash((self._ArrowHeads, self._Leaders))

    def __repr__(self):
        return "".join(["DimensionalLine (", str(self._ArrowHeads), "), Leaders (", str(self._Leaders),")"])

    @staticmethod
    def ExtractDimensionalLine(self,arrows, leaders):
        self._ArrowHeads = arrows
        self._Leaders = leaders

class DimensionalTexts():

    def __init__(self):
        self._Text = "AdityaIntwala"
        self._TextBoxP1 = Point2(0,0)
        self._TextBoxP2 = Point2(0,0)
        self._Orientation = 90        

    def __hash__(self):
      return hash((self._Text, self._TextBoxP1, self._TextBoxP2, self._Orientation))

    def __repr__(self):
        return "".join(["DimensionalText ( Text = ", str(self._Text), ", P1 = ", str(self._TextBoxP1),", P2 = ", str(self._TextBoxP2),", Orientation = ", str(self._Orientation),")"])

    @staticmethod
    def ExtractDimensionalText(self, dimensionText, p1, p2, orientationAngle):
        self._Text = dimensionText
        self._TextBoxP1 = p1
        self._TextBoxP2 = p2
        self._Orientation = orientationAngle

class Dimensions():

    def __init__(self):
      self._DimensionalLines = DimensionalLines()  
      self._DimensionalText = DimensionalTexts()
      self._SupportLines = []

       
    def __hash__(self):
      return hash((self._DimensionalLines, self._DimensionalText, self._SupportLines))

    def __repr__(self):
        return "".join(["Dimension (", str(self._DimensionalLines), "), (", str(self._DimensionalText), ")", ", (", str(self._SupportLines), ")"])
    
    @staticmethod   
    def ExtractDimension(self, Dimensionallines, Dimensionaltext ):
        self._DimensionalLines = Dimensionallines
        self._DimensionalText = Dimensionaltext

class CorrelatedEntity():

    def __init__(self):
      self._Dimension = Dimensions()  
      self._Entity = []
       
    def __hash__(self):
      return hash((self._Dimension, self._Entity))
    
    def __repr__(self):
        return "".join(["CorrelatedEntity (", str(self._Dimension), "), (", str(self._Entity), ")"])

    @staticmethod   
    def ExtractCorrelatedEntity(self, Dim, cEntity ):
        self._Dimension = Dim
        self._Entity = cEntity
        
class ExtractedLines():
    _rho = 0
    _theta = 0
    _p1 = Point2(0,0)
    _p2 = Point2(0,0)

    def __init__(self):
        self._rho = 0
        self._theta = 0
        self._p1 = Point2(0,0)
        self._p2 = Point2(0,0)

    def __eq__(self, other):
        tol = 1.0
        return (fabs(self._rho - other._rho) < tol and fabs(self._theta - other._theta) < tol )

    def __hash__(self):
      return hash((self._rho, self._theta, self._p1, self._p2))

    def __repr__(self):
        return "".join(["line (rho =", str(self._rho), ", theta =", str(self._theta),", Point1 = ", str(self._p1),", Point2 =", str(self._p2), ")"])
    
    @staticmethod   
    def ExtractLine(self,rho, theta, p1, p2):
        self._rho = rho
        self._theta = theta
        self._p1 = p1
        self._p2 = p2

class ExtractedCircles():
    _centre = Point2(0,0)
    _radius = 0

    def __init__(self):
        
        self._centre = Point2(0,0)
        self._radius = 0
        self._pixels = []

    def __eq__(self, other):
        tol = 4.0
        return (fabs(self._centre - other._centre) < tol and fabs(self._radius - other._radius) < tol )

    def __hash__(self):
      return hash((self._centre, self._radius))

    def __repr__(self):
        return "".join(["Circle (Centre =", str(self._centre), ", Radius =", str(self._radius), ")"])
    
    @staticmethod   
    def ExtractCircle(self,centre, radius):
        self._centre = centre
        self._radius = radius
        
class ExtractedText():

    _p1 = Point2(0,0)
    _p2 = Point2(0,0)
    _text = ""
    _cropedImg = np.zeros([100,100,3],dtype=np.uint8)

    def __init__(self):
        
        self._p1 = Point2(0,0)
        self._p2 = Point2(0,0)
        self._text = ""
        self._cropedImg = np.zeros([100,100,3],dtype=np.uint8)

    def __hash__(self):
      return hash((self._p1, self._p2, self._text, self._cropedImg))

    def __repr__(self):
        return "".join(["ExtractedText p1=", str(self._p1), ", p2 =", str(self._p2),", DetectedText = ", str(self._text),", PathOfImg =", str(self._cropedImg), ")"])
    
    @staticmethod   
    def ExtractText(self,p1, p2, text, path):
        self._p1 = p1
        self._p2 = p2
        self._text = text
        self._cropedImg = path

class FeatureManager():

    def __init__(self):
        self._DetectedArrowHead = ArrowHeads()
        self._DetectedDimensionalLine = DimensionalLines()
        self._DetectedDimensionalText = DimensionalTexts()
        self._DetectedDimension = Dimensions()
        self._DetectedLine = []
        self._DetectedCircle = ExtractedCircles()
        self._CorrelatedEntities = CorrelatedEntity()
        self._ImagePath = "TestData/BOOK/FinalTestImages/1.png"
        self._RootDirectory = "Output/temp/"
        self._ImageOriginal = np.zeros((3,3), dtype = np.uint8)
        self._ImageCleaned = np.zeros((3,3), dtype = np.uint8)
        self._ImageDetectedArrow = np.zeros((3,3), dtype = np.uint8)
        self._ImageDetectedDimensionalLine = np.zeros((3,3), dtype = np.uint8)
        self._ImageDetectedDimensionalText = np.zeros((3,3), dtype = np.uint8)
        self._ImageDetectedLine = np.zeros((3,3), dtype = np.uint8)
        self._ImageDetectedCircle = np.zeros((3,3), dtype = np.uint8)