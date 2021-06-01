# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 17:35:18 2020

@author: KIIT
"""
#When using spyder just use import cv2 but for VSCode use from cv2 import cv2
from cv2 import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import math
import sys
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def hrtRate(vidP,vidT):
    #This method is used to count the total number of freames, it takes the path 
    #of the video as a parameter and iterates till the end of video
    def countFrames(videoPath):
        vid = cv2.VideoCapture(videoPath)
        nof = 0
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            nof=nof+1
            
        vid.release()
        return nof
    #This method is used to make subplots
    def make_plot(axs, tFrame, data, j, s):
        plt.figure(num=None, figsize=(12, 8), dpi=1200, facecolor='w', edgecolor='k')
        axs[j].plot(tFrame,data)
        axs[j].set_title(s)

    '''
    Variables are declares here
    '''
    #Storing the path of the video
    vidPath = vidP
    #Creation of an object that stores the video file in form of multidimensional
    #matrix
    vidObj = cv2.VideoCapture(vidPath)
    #Calculation the total number of frames in the video
    nFrames = int(countFrames(vidPath))   
    #Calculation the frames per second of the video
    fps = int(vidObj.get(cv2.CAP_PROP_FPS))
    if fps == 31 or fps == 61:
        fps=fps-1
    #This array is also intialized to zero which will be used to store the time 
    #period
    #tFrame = np.zeros(nFrames)
    #User input for total video time
    vidTime = int(vidT)
    print(vidTime)
    #Total number of frames with respect to vidTime
    totalLen = int(vidTime * (fps + 1))


    newVidPath = 'trim.mp4'
    fileExists = os.path.exists('trim.mp4')
    if(fileExists):
        os.remove('trim.mp4')

    ffmpeg_extract_subclip(vidPath, 0, 0 + vidTime,targetname = 'trim.mp4')

    newVidObj = cv2.VideoCapture('trim.mp4')

    """
    if(nFrames < totalLen):
        print("Invalid video input")
        print("Error: Video Length too small")
        sys.exit()
    """
    i = 0

    nFrames = int(countFrames(newVidPath))
    gData = np.zeros(nFrames)
    fps = int(newVidObj.get(cv2.CAP_PROP_FPS) + 1)
    if fps == 31 or fps == 61:
        fps=fps-1
    tFrame = np.zeros(nFrames)

    for i in range(nFrames):
        tFrame[i] = (i+1) / fps

    #Fail check in case of corrupted video file
    if(newVidObj.isOpened()==False):
        print("Error opening the video file.")
        sys.exit()

    i=0
    #Converting the video input to grayscaled, which is stored in gData in form of 
    #2d matrix
    while(True):
        ret, frame = newVidObj.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gData[i] = np.sum(gray)
        i+=1

    """
    RISKY RECTIFICATION ATTEMPT
    """

    rectifiedGraph = gData

    #For first 0.5 seconds if the fps is lets say 30 then the number of frames in
    #05 seconds will  be 0.5 x 30 = 15 frames

    framesPerBatch = int(0.5 * fps)
    min_var = sys.maxsize * 2 + 1
    max_var = -min_var - 1
    k=0
    while k < framesPerBatch:
        if rectifiedGraph[k] >= max_var:
            max_var = rectifiedGraph[k]
        elif rectifiedGraph[k] <= min_var:
            min_var = rectifiedGraph[k]
        k = k + 1

    median = int((max_var + min_var)/2)
    deviation = 0
    i=0
    j=0
    k=0
    rGraph = np.zeros(nFrames)
    while i < nFrames:
        min_var = sys.maxsize * 2 + 1
        max_var = -min_var - 1
        k=i
        while k < i + framesPerBatch:
            if k >= nFrames:
                break
            if rectifiedGraph[k] >= max_var:
                max_var = rectifiedGraph[k]
            elif rectifiedGraph[k] <= min_var:
                min_var = rectifiedGraph[k]
            k = k + 1
        batch_median = int((max_var + min_var)/2)
        deviation = int(median - batch_median)
        while j < i + framesPerBatch:
            if j >= nFrames:
                break
            rGraph[j] = rectifiedGraph[j] + deviation
            j = j + 1
        i = i + framesPerBatch
            


    """
    RISKY RECTIFICATION ATTEMPT
    """

    rGraph[nFrames - 1] = rGraph[nFrames - 2]

    #Filtering the data with median filter to remove unwanted noise with a factor 
    #of 9
    fData = medfilt(rGraph,5)

    #A threshold is created to recify the plot
    g_max = np.amax(fData)
    g_min = np.amin(fData)
    offset = int(g_max - g_min)
    threshold = (g_min) + (0.55*offset)

    #The threshold is used to rectify the plot into a square wave
    sqData = medfilt(rGraph,5)
    i=0
    for i in range(nFrames):
        if sqData[i] <= threshold:
            sqData[i] = 1
        else:
            sqData[i] = 0

    #Now the number of peaks is calculated which is done by calculating number of 
    #changes in the square wave and dividing it by 2
    c=0
    i=1
    prev = sqData[0]
    for i in range(nFrames):
        if sqData[i] != prev:
            c = c+1
            prev = sqData[i]
        else:
            prev = sqData[i]


    #Finally the wave is plotted
    #plt.title("HR Graph")
    #plt.xlabel("xlabel")
    #plt.ylabel("ylabel")
    #plt.plot(tFrame,sqData)

    #Creating a pane for plotting 4 different graphs
    fig, axs = plt.subplots(4)
    fig.tight_layout(h_pad = 2)
    fig.suptitle('Heart Rate')
    plt.subplots_adjust(top=0.85)
    make_plot(axs, tFrame, gData,0, "First Plot")
    make_plot(axs, tFrame, rGraph, 1, "Corrected Plot")
    make_plot(axs, tFrame, fData, 2, "Filtered Plot")
    make_plot(axs, tFrame, sqData, 3, "Square Plot")

    fileExists = os.path.exists('static\\out.png')
    if(fileExists):
        os.remove('static\\out.png')

    fig.savefig('static\\out.png',dpi = 1200)

    #Since the video taken is of 10 seconds the counter is multiplied by a factor 
    #of 6 in order to get heart beats per minute
    multiplying_factor = int(60 / vidTime)
    hrm = math.ceil(c/2) * multiplying_factor
    print(hrm)




    #Resources is being freed here
    vidObj.release()
    newVidObj.release()
    cv2.destroyAllWindows()

    fileExists = os.path.exists('trim.mp4')
    if(fileExists):
        os.remove('trim.mp4')

    return hrm
