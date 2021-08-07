# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import cv2
import numpy as np
from math import sqrt
from skimage.transform import radon
from numpy import mean, array, argmax

class ImgTransform():

    def rms_flat(a):
        return np.sqrt(np.mean(np.absolute(a)**2))

    @staticmethod
    def OrientationAngle(img):
        I = img
        I = I - mean(I)     
        sinogram = radon(I)        
        r = array([ImgTransform.rms_flat(line) for line in sinogram.transpose()])
        rotation = argmax(r)
  
        OrientationAngle = rotation - 90
        return OrientationAngle

    @staticmethod
    def ImgRotate(img, angle, scale):
        if (len(img.shape) == 2):
            rows,cols = img.shape
            diagonal = int(sqrt((rows * rows) + (cols * cols)))
            X_offset = int((diagonal - rows)/2)
            Y_offset = int((diagonal - cols)/2)
            rot_img = np.zeros((diagonal, diagonal), dtype = 'uint8')
            img_center = (diagonal/2, diagonal/2)
            rot_img.fill(255)
            rotateMatrix = cv2.getRotationMatrix2D(img_center, angle, scale)
            rot_img[X_offset:(X_offset + rows), Y_offset:(Y_offset + cols)] = img 
            rot_img = cv2.warpAffine(rot_img, rotateMatrix, (diagonal, diagonal), flags = cv2.INTER_LINEAR, borderMode = cv2.BORDER_CONSTANT,borderValue = (255,255,255))
        else:
            rows,cols,channels = img.shape
            diagonal = int(sqrt((rows * rows) + (cols * cols)))
            X_offset = int((diagonal - rows)/2)
            Y_offset = int((diagonal - cols)/2)
            rot_img = np.zeros((diagonal, diagonal,channels), dtype = 'uint8')
            rot_img.fill(255)
            
            img_center = (diagonal/2, diagonal/2)
       
            rotateMatrix = cv2.getRotationMatrix2D(img_center, angle, scale)
            rot_img[X_offset:(X_offset + rows), Y_offset:(Y_offset + cols)] = img        
            rot_img = cv2.warpAffine(rot_img, rotateMatrix, (diagonal, diagonal), flags = cv2.INTER_LINEAR, borderMode = cv2.BORDER_CONSTANT,borderValue = (255,255,255))
       
        return rot_img


    @staticmethod
    def ImgTranslate(img, tx, ty):
        rows,cols = img.shape
        Translatematrix = np.float32([[1,0,tx],[0,1,ty]])
        trans_img = cv2.warpAffine(img, Translatematrix, (cols,rows))

        return trans_img

    @staticmethod
    def ImgCrop(img, x, y, w, h):
        crop_img = img[y:h, x:w]
        return crop_img

    @staticmethod
    def ImgFlipVertical(img):
        flipV_img = cv2.flip(img,1)
        return flipV_img

    @staticmethod
    def ImgFlipHorizontal(img):
        flipH_img = cv2.flip(img,0)
        return flipH_img

    @staticmethod
    def ImgAspectResize(img,h,w):
        if h == None:
            r = w / img.shape[1]
            dim = (w, int(img.shape[0] * r))
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            return resized
        if w == None:
            r = h / img.shape[0]
            dim = (int(img.shape[1] * r), h)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            return resized
        if (h != None and w != None):
            rw = w / img.shape[1]
            rh = h / img.shape[0]
            dim = ( int(img.shape[1] * rh), int(img.shape[0] * rw))
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            return resized

    @staticmethod
    def ImgAffine(img, pts1, pts2):
        rows,cols = img.shape
        Affinematrix = cv2.getAffineTransform(pts1,pts2)
        affine = cv2.warpAffine(img, Affinematrix, (cols,rows))
        return affine

    @staticmethod
    def ImgPerspective(img, pts1, pts2):
        rows,cols = img.shape
        Perspectivematrix = cv2.getPerspectiveTransform(pts1,pts2)
        perspective = cv2.warpPerspective(img, Perspectivematrix, (cols,rows))
        return perspective
    



         
        

