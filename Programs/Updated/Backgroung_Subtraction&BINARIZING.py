#---------------------------------------------------IMPORTING LIBRARIES-------------------------------------------------------------------------------
import cv2
import numpy as np


#---------------------------------------------------------------------------------------------------------------------------------
cap=cv2.VideoCapture("C:/Users/HIMA/Desktop/PROJECTS/CBIR/Vehicle_Detection-And-Classification/video.mp4")

#Intialize Subtractor
algo=cv2.bgsegm.createBackgroundSubtractorMOG()

while(True):
    ret,frame1=cap.read()
    grey=cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(grey,(3,3),5)
    #applying on each frame
    img_sub=algo.apply(blur)
    dilat=cv2.dilate(img_sub,np.ones((5,5)))
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilatada=cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)
    counterShape=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("DECTECTOR",dilatada)

    if cv2.waitKey(1)==13:
        break

cv2.destroyAllWindows()
cap.release()