# Image2CAD
A prototype application to translate a raster image of CAD drawing to user editable DXF CAD format, using concepts of image processing and Machine Learning. This is based on the paper [Image to CAD: Feature Extraction and Translation of Raster Image of CAD Drawing to DXF CAD Format](/Paper/Image2CAD_AdityaIntwala_CVIP2019.pdf) by Aditya Intwala.

The idea is to make the open-sourced version more robust and accurate with integrating the Machine Learning models for the individual stages of current pipeline similar to original version but more accurate and robust with the help of collaboration.

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

## Introduction
A CAD drawing has various drawing features like entity lines, dimensional lines, dimensional arrows, dimensional text, support lines, reference lines, Circles, GD&T symbols and drawing information metadata. The problem of automated or semi-automated recognition of feature entities from 2D CAD drawings in the form of raster images has multiple usages in various scenarios. The present research work explores the ways to extract this information about the entities from 2D CAD drawings raster images and to set up a workflow to do it in automated or semi-automated way. The algorithms and workflow have been tested and refined using a set of test CAD images which are fairly representative of the CAD drawings encountered in practice. The overall success rate of the proposed process is 90% in fully automated mode for the given sample of the test images. The prototype is used to generate user editable DXF CAD file from raster images of CAD drawings which could be then used to update/edit the CAD model when required using CAD packages. The current work is a stripped-down version of original work presented in paper; this might not reproduce same results as the paper but the workflow is highly relatable to the original pipeline. The stripped-down version has not got the generalization, robustness or the stability of the original version. 


