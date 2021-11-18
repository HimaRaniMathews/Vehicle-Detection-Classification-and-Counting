import cv2
import numpy as np
import time

#---------------------------------------------------VARIABLE DECLARATIONS-------------------------------------------------------------------------------
cap=cv2.VideoCapture("./Videos/video.mp4")
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=False,history=200,varThreshold = 90)
while(cap.isOpened()):
    ret,frame=cap.read() 
    frame=cv2.resize(frame,(900,500))
    fgmask=fgbg.apply(frame)

#------------------------------------------------------BINARIZATION----------------------------------------------------------------------------
    if ret==True:
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        cv2.imshow('Thresholding',imBin)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    

cap.release()
cv2.destroyAllWindows()
