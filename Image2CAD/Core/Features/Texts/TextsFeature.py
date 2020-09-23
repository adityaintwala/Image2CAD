# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:01:10 2020

@author: Aditya Intwala
"""


import cv2
import numpy as np
import os
from Math import Point2
from ConnectedComponents.ConnectedComponents import ConnectedComponent
from FeatureManager import DimensionalTexts
from Utils.ImgTransform import ImgTransform
from .Cognition.Cognition import Cognition
import pytesseract
from PIL import Image

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

class TextsFeature:

    global make_dir_roi, make_dir_rotate, timestr, DimensioanlLines

    @staticmethod
    def Make_Directory(makedir_root):
        global make_dir_roi, make_dir_rotate, timestr
        make_dir_roi = makedir_root + "/SegmentedText"
        make_dir_rotate = makedir_root + "/RotatedText"
        os.mkdir(make_dir_roi)
        os.mkdir(make_dir_rotate)
               

    @staticmethod
    def Arrow_Deleter(blank_img):
        invt_img = cv2.bitwise_not(blank_img)
        return invt_img

    @staticmethod
    def Contour_Find(invt_img):
        Kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))        
        open_img = cv2.morphologyEx(invt_img, cv2.MORPH_OPEN, Kernel_rect)
        open_img = cv2.bitwise_not(open_img)
        open_img = cv2.cvtColor(open_img,cv2.COLOR_BGR2GRAY)
        ret, thresh_img = cv2.threshold(open_img,190,255,cv2.THRESH_BINARY)
        cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        return cnts
    
    @staticmethod
    def Extract_Text(img, cnts):
        global DimensioanlLines
        i = 0
        ExtractedTextArea = []
        RotatedText = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            crWidth = w / float(img.shape[1])
            area = cv2.contourArea(c)            
            if  h > 5 and w > 4 and ar > 0.4 and 0.5>crWidth > 0.001 and area>20: 
                roi = img[y:y + h+1, x:x + w+1].copy()   
                Rotate_roi = img[y:y + h+5, x:x + w+5].copy()   
                cv2.imwrite(make_dir_roi + "/segmentedtext"+str(i)+".png",roi)
                BB = [x, y, w, h]       
                new_img = TextsFeature.Paste(img,roi)  
                OrientationAngle = ((Cognition.GetOrientation(DimensioanlLines,BB)))
                output_img_path, detected_text =  TextsFeature.RotateByAngle( new_img,OrientationAngle, make_dir_rotate, i)
                p1 = Point2(x-2, y-2)
                p2 = Point2(x + w+2, y + h+2)
                DimText = DimensionalTexts()
                DimText.ExtractDimensionalText(DimText, detected_text, p1, p2, OrientationAngle)
                ExtractedTextArea.append(DimText)
                i += 1
    
        return ExtractedTextArea, RotatedText
    
    @staticmethod
    def Draw_BB(output_img, ExtractedTextArea):
        for textarea in ExtractedTextArea:
            p1 = textarea._TextBoxP1
            p2 = textarea._TextBoxP2
            cv2.rectangle(output_img, (p1.x, p1.y), (p2.x, p2.y), (0, 255, 0), 2)
        return output_img
    
    @staticmethod
    def Paste(img,roi):
        new_img = np.zeros([303,279,3], np.uint8)
        new_img.fill(255)
        rows,cols,channels = roi.shape
        New_Img_roi = new_img[0:rows, 0:cols ]
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(roi_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        New_Img_bg = cv2.bitwise_and(New_Img_roi, New_Img_roi, mask = mask_inv)
        New_Img_fg = cv2.bitwise_and(roi, roi, mask = mask)
        dst = cv2.add(New_Img_bg, New_Img_fg)
        new_img[150:150+rows, 150:150+cols ] = dst

        return new_img
    
    @staticmethod
    def ccDetect(img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh_img = cv2.threshold(gray_img,190,255,cv2.THRESH_BINARY)
        blank_img = np.zeros(img.shape, np.uint8)
        labels, ccImg = ConnectedComponent.detect(thresh_img)
        SortedLabels = {}
        for key, value in sorted(labels.items()):
            SortedLabels.setdefault(value, []).append(key)
        for i in range(0,2):            #range(0,3) changed on 18-2-16
            maxCCkey=max(SortedLabels, key=lambda k: len(SortedLabels[k]))
            SortedLabels.pop(maxCCkey)
        
        for i in SortedLabels.values():
            for j in i:
                blank_img[j[0],j[1]] = 255
        

        return SortedLabels, blank_img
    
    @staticmethod
    def RotateByAngle(new_img, angle, make_dir_rotate, i ):
        rotate_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        rotate_img = ImgTransform.ImgRotate(rotate_img,angle,1)
        rotate_img = ImgTransform.ImgAspectResize(rotate_img,800,800)
        output_img_path = make_dir_rotate + "/rotate" + str(i) + ".png"
        cv2.imwrite(output_img_path, rotate_img)
        detected_text = pytesseract.image_to_string(Image.open(output_img_path), lang='eng+eng13', psm = '6')
               
        return output_img_path, detected_text
    
    @staticmethod
    def Detect(Feature_Manager):
        global DimensioanlLines
        make_dir_root = Feature_Manager._RootDirectory
        DimensioanlLines = Feature_Manager._DetectedDimensionalLine
        img = Feature_Manager._ImageOriginal.copy()
        output_img = img.copy()
        TextsFeature.Make_Directory(make_dir_root)       
        labels, blank_img = TextsFeature.ccDetect(img)
        invt_img = TextsFeature.Arrow_Deleter(blank_img)
        cnts = TextsFeature.Contour_Find(invt_img)
        ExtractedTextArea, RotatedText = TextsFeature.Extract_Text(img, cnts)
        output_img = TextsFeature.Draw_BB(output_img, ExtractedTextArea)
        cv2.imwrite(make_dir_root + "/Text_Extraction_Output.png",output_img)

        return ExtractedTextArea, output_img
    
    @staticmethod
    def Dump(make_dir_root, time, TextAreaList):
        Root = Element("Root")
        Extracted_Text_Area = SubElement(Root, "Extracted_Text_Area")
        i = 0
        for item in TextAreaList:
            Extracted_Text = SubElement(Extracted_Text_Area, "Extracted_Text")
            Extracted_Text.text = str(i)
            Detected_Text = SubElement(Extracted_Text, "Detected_Text")
            Detected_Text.text = item._Text
            BB_Min_Point = SubElement(Extracted_Text, "BB_Min_Point")
            Min_Point_x = SubElement(BB_Min_Point, "x")
            Min_Point_x.text = str(item._TextBoxP1.x)
            Min_Point_y = SubElement(BB_Min_Point, "y")
            Min_Point_y.text = str(item._TextBoxP1.y)
            BB_Max_Point = SubElement(Extracted_Text, "BB_Max_Point")
            Max_Point_x = SubElement(BB_Max_Point, "x")
            Max_Point_x.text = str(item._TextBoxP2.x)
            Max_Point_y = SubElement(BB_Max_Point, "y")
            Max_Point_y.text = str(item._TextBoxP2.y)
            Orientation_Angle = SubElement(Extracted_Text, "Orientation_Angle")
            Orientation_Angle.text = str(item._Orientation)
            i += 1
           
        tree = ET.ElementTree(Root)
        tree.write(make_dir_root +"/Text_Extraction.xml")


