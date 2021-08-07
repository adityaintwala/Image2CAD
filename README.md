# Image2CAD
Copyright (C) 2016, Aditya Intwala.

A prototype application to translate a raster image of CAD drawing to user editable DXF CAD format, using concepts of Image Processing and Machine Learning. This is based on the paper [Image to CAD: Feature Extraction and Translation of Raster Image of CAD Drawing to DXF CAD Format](/Paper/Image2CAD_AdityaIntwala_CVIP2019.pdf) by Aditya Intwala.

The idea is to make the open-sourced version more robust and accurate with integrating the Machine Learning models for the individual stages of current pipeline similar to original version but more accurate and robust with the help of collaboration.

The opensourced version is slightly different than what is presented in the paper. The OCR in original version was hand tailored for Mechanical drawings fonts and GD&T symbols which was more accurate than present Tessaract OCR. This version is based on OpenCV 3.0 while original was based on OpenCV 2.0.

## Demo Video
[![Image 2 CAD Demo](/Paper/Image2CAD.gif)](https://youtu.be/Isxtcwe57cc)


## Cite
Please cite the below research if using as is or with any modification in your research.
```
@inproceedings{intwala2019image,
  title={Image to CAD: Feature Extraction and Translation of Raster Image of CAD Drawing to DXF CAD Format},
  author={Intwala, Aditya},
  booktitle={International Conference on Computer Vision and Image Processing},
  pages={205--215},
  year={2019},
  organization={Springer}
}
```
## Contribution Guidelines
Please get in touch with the author for contribution related queries.

## Introduction
A CAD drawing has various drawing features like entity lines, dimensional lines, dimensional arrows, dimensional text, support lines, reference lines, Circles, GD&T symbols and drawing information metadata. The problem of automated or semi-automated recognition of feature entities from 2D CAD drawings in the form of raster images has multiple usages in various scenarios. The present research work explores the ways to extract this information about the entities from 2D CAD drawings raster images and to set up a workflow to do it in automated or semi-automated way. The algorithms and workflow have been tested and refined using a set of test CAD images which are fairly representative of the CAD drawings encountered in practice. The overall success rate of the proposed process is 90% in fully automated mode for the given sample of the test images. The prototype is used to generate user editable DXF CAD file from raster images of CAD drawings which could be then used to update/edit the CAD model when required using CAD packages. The current work is a stripped-down version of original work presented in paper; this might not reproduce same results as the paper but the workflow is highly relatable to the original pipeline. The stripped-down version has not got the generalization, robustness or the stability of the original version. 

## Usage
''' python Image2CAD.py ..//TestData//1.png '''

### Input
The script requires one positional argument and few optional parameters:
* image_path - Complete path to the image file of CAD drawing.

### Output
The output of the script would be multiple files:
* *.I2C - A custom Image2CAD file conatining extracted and corelated feature information which than can be processed to DXF file.
* *.png - Multiple output images of various individual feature detected.

## Arrowhead Feature Detection
Input Image  |  Detected Arrowheads Output Image 
:------------------:|:--------------------:
![Input Image](/TestData/1.png)  |  ![Detected Arrowheads Output Image](/TestData/Output/1/20201120-093555/Arrowheads_Extraction_Output.png)
![Input Image](/TestData/2.PNG)  |  ![Detected Arrowheads Output Image](/TestData/Output/2/20201120-093813/Arrowheads_Extraction_Output.png)
![Input Image](/TestData/3.PNG)  |  ![Detected Arrowheads Output Image](/TestData/Output/3/20201120-093906/Arrowheads_Extraction_Output.png)
![Input Image](/TestData/4.PNG)  |  ![Detected Arrowheads Output Image](/TestData/Output/4/20201120-093947/Arrowheads_Extraction_Output.png)

## Dimensional Line Feature Detection
Input Image  |  Detected Dimensional Lines Output Image 
:------------------:|:--------------------:
![Input Image](/TestData/1.png)  |  ![Detected Dimensional Lines Output Image](/TestData/Output/1/20201120-093555/DimensionalLine_Extraction_Output.png)
![Input Image](/TestData/2.PNG)  |  ![Detected Dimensional Lines Output Image](/TestData/Output/2/20201120-093813/DimensionalLine_Extraction_Output.png)
![Input Image](/TestData/3.PNG)  |  ![Detected Dimensional Lines Output Image](/TestData/Output/3/20201120-093906/DimensionalLine_Extraction_Output.png)
![Input Image](/TestData/4.PNG)  |  ![Detected Dimensional Lines Output Image](/TestData/Output/4/20201120-093947/DimensionalLine_Extraction_Output.png)

## Dimensional Text Feature Detection
Input Image  |  Detected Dimensional Text Output Image 
:------------------:|:--------------------:
![Input Image](/TestData/1.png)  |  ![Detected Dimensional Text Output Image](/TestData/Output/1/20201120-093555/Text_Extraction_Output.png)
![Input Image](/TestData/2.PNG)  |  ![Detected Dimensional Text Output Image](/TestData/Output/2/20201120-093813/Text_Extraction_Output.png)
![Input Image](/TestData/3.PNG)  |  ![Detected Dimensional Text Output Image](/TestData/Output/3/20201120-093906/Text_Extraction_Output.png)
![Input Image](/TestData/4.PNG)  |  ![Detected Dimensional Text Output Image](/TestData/Output/4/20201120-093947/Text_Extraction_Output.png)

## Line Feature Detection
Input Image  |  Detected Lines Output Image 
:------------------:|:--------------------:
![Input Image](/TestData/1.png)  |  ![Detected Lines Output Image](/TestData/Output/1/20201120-093555/Line_Extraction_Output.png)
![Input Image](/TestData/2.PNG)  |  ![Detected Lines Output Image](/TestData/Output/2/20201120-093813/Line_Extraction_Output.png)
![Input Image](/TestData/3.PNG)  |  ![Detected Lines Output Image](/TestData/Output/3/20201120-093906/Line_Extraction_Output.png)
![Input Image](/TestData/4.PNG)  |  ![Detected Lines Output Image](/TestData/Output/4/20201120-093947/Line_Extraction_Output.png)

## Circle Feature Detection
Input Image  |  Detected Circles Output Image 
:------------------:|:--------------------:
![Input Image](/TestData/1.png)  |  ![Detected Circles Output Image](/TestData/Output/1/20201120-093555/Circle_Extraction_Output.png)

## Major Dependencies
* OpenCV 3.4.2
* TessaractOCR 
* ezdxf
* numpy
* scipy