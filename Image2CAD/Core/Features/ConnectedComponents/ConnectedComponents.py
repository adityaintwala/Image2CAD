# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
import random
from itertools import product

class UnionFind_array:

    def __init__(self):
        self.A = []
        self.label = 0

    def Create_Label(self):
        new_label = self.label
        self.label += 1
        self.A.append(new_label)
        return new_label

    def Find_Root(self, i):
        while self.A[i] < i:
            i = self.A[i]
        return i

    def Find(self, i):
        root = self.Find_Root(i)
        self.Set_Root(i, root)
        return root

    def Set_Root(self, i, root):
        while self.A[i] < i:
            j = self.A[i]
            self.A[i] = root
            i = j
        self.A[i] = root
   
    def Union(self, i, j):
        if i != j:
            root = self.Find_Root(i)
            rootj = self.Find_Root(j)
            if root > rootj: root = rootj
            self.Set_Root(j, root)
            self.Set_Root(i, root)
    
    def Flatten(self):
        for i in range(1, len(self.A)):
            self.A[i] = self.A[self.A[i]]
    
    def FlattenL(self):
        k = 1
        for i in range(1, len(self.A)):
            if self.A[i] < i:
                self.A[i] = self.A[self.A[i]]
            else:
                self.A[i] = k
                k += 1


class ConnectedComponent:

    def Detect(img):
       
        width, height = img.shape
        output_img = img.copy()
        output_img = cv2.cvtColor(output_img, cv2.COLOR_GRAY2BGR)
       
        ua = UnionFind_array()
       
        labels = {}
     
        for y, x in product(range(height), range(width)):
           
            if img.item(x,y) == 255:
                pass

            elif y > 0 and img.item(x, y-1) == 0:
                labels[x, y] = labels[(x, y-1)]

            elif x+1 < width and y > 0 and img.item(x+1, y-1) == 0:
                c = labels[(x+1, y-1)]
                labels[x, y] = c
                
                if x > 0 and img.item(x-1, y-1) == 0:
                    a = labels[(x-1, y-1)]
                    ua.Union(c, a)

                elif x > 0 and img.item(x-1, y) == 0:
                    d = labels[(x-1, y)]
                    ua.Union(c, d)

            elif x > 0 and y > 0 and img.item(x-1, y-1) == 0:
                labels[x, y] = labels[(x-1, y-1)]

            elif x > 0 and img.item(x-1, y) == 0:
                labels[x, y] = labels[(x-1, y)]

            else: 
                labels[x, y] = ua.Create_Label()
     
        ua.Flatten()
     
        colors = {}

        for (x, y) in labels:

            component = ua.Find(labels[(x, y)])
    
            labels[(x, y)] = component
     
            if component not in colors: 
                colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
    
            output_img[x, y] = colors[component]
    
        return (labels, output_img)

