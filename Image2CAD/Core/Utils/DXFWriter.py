# -*- coding: utf-8 -*-
"""
@author: Aditya Intwala

 Copyright (C) 2016, Aditya Intwala.

 Licensed under the Apache License 2.0. See LICENSE file in the project root for full license information.
"""

import os
import ezdxf

class DXFWriter:

       @staticmethod
       def Write(Feature_Manager):
           dxfFileName = os.path.splitext(os.path.basename(Feature_Manager._ImagePath))[0]
           dxfFilePath = Feature_Manager._RootDirectory + "/" + dxfFileName +".dxf"
           
           drawing = ezdxf.new('R2010')
           msp = drawing.modelspace()
           
           for L in Feature_Manager._DetectedLine:
               if(L.endPoint == L.startPoint):
                   continue
               msp.add_line((L.startPoint.x, L.startPoint.y), (L.endPoint.x, L.endPoint.y))
               offset = 4
               dim = msp.add_aligned_dim(p1=(L.startPoint.x, L.startPoint.y), p2=(L.endPoint.x, L.endPoint.y), distance=offset) #, text='DimText'
               dim.set_arrows(blk=ezdxf.ARROWS.closed_filled, size=1)
               dim.render()
               
           for C in Feature_Manager._DetectedCircle:
               msp.add_circle(center=(C._centre.x, C._centre.y), radius=C._radius)
               dim = msp.add_radius_dim(center=(C._centre.x, C._centre.y), radius=C._radius, angle=45, dimstyle='EZ_RADIUS')
               dim.render()
           
           drawing.saveas(dxfFilePath)