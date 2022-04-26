#File Name: MaskResize.py
#Primary Contributor: Coby Kromis
#Other Contributors: 
#Purpose: This file is used for the purpose of masking and resaving images with specifications
#related to fertilization and gender detection project

import py_compile

import cv2 as cv
import sys
import numpy as np
import os
from matplotlib import pyplot as plt
from patchify import patchify

#HSV in OpenCV is H: 0-179, S: 0-255, V: 0-255

#HSV Yellow Threshold
YH = np.array([25, 255, 255])
YL = np.array([15, 75, 150])

#HSV Orange Threshold
OH = np.array([179, 255, 255])
OL = np.array([0, 110, 110])

#Resize percentage value and original size values
RESIZE = 25
OGH = 4032
OGW = 3024

#Uses patchify library to reduce original image down to 256x256 size
def sizeChange(img, oh, ow):
    rImg = img

    if img.shape == (oh, ow):
        rImg = patchify(img, (256, 256), step=256)

    return rImg

#Mask for brown eggs - THey glow orange in the candling process
def oMask(path):
    img = cv.imread(path)

    if img is None:
        sys.exit("Image not found\n")

    #Convert image to hsv color space from BGR and then mask it
    hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvImg, OL, OH)
    maskImg = cv.bitwise_and(img, hsvImg, mask = mask)

    rmImg = sizeChange(maskImg, OGH, OGW)

    #resave masked and resized image into original file location
    cv.imwrite(path, rmImg)

#Mask for white eggs - They glow yellow in the candling process
def yMask(path):
    img = cv.imread(path)

    if img is None:
        sys.exit("Image not found\n")

    #Convert image to hsv color space from BGR and then mask it
    hsvImg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvImg, YL, YH)
    maskImg = cv.bitwise_and(img, hsvImg, mask = mask)

    rmImg = sizeChange(maskImg, OGH, OGW)
    
    #resave masked and resized image into original file location
    cv.imwrite(path, rmImg)