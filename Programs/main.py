#---------------------------------------------------IMPORTING LIBRARIES-------------------------------------------------------------------------------
import cv2
import numpy as np
import time
import vehicles

#---------------------------------------------------VARIABLE DECLARATIONS-------------------------------------------------------------------------------
cap=cv2.VideoCapture("./Videos/video.mp4") 
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=False,history=200,varThreshold = 90)
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_p_age = 5
pid = 1
cnt_up=0
cnt_down=0
line_up=400
line_down=250
up_limit=230
down_limit=int(4.5*(500/5))


print("VEHICLE DETECTION,CLASSIFICATION AND COUNTING")

#---------------------------------------------------RETRIEVING VEHICLES-------------------------------------------------------------------------------
if (cap.isOpened()== False):
  print("Error opening video stream or file")

while(cap.isOpened()):
    ret,frame=cap.read() 
    frame=cv2.resize(frame,(900,500))
    for i in cars:
        i.age_one()
    fgmask=fgbg.apply(frame)

#------------------------------------------------------BINARIZATION----------------------------------------------------------------------------
    if ret==True:
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp) #Opening :E->D
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl) #Closing :D->E

        (contours0,hierarchy)=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #Contour Extraction
        for cnt in contours0:
            area=cv2.contourArea(cnt)
            #print(area) #Printing the Area of each Object 
            
            if area>300:
                m=cv2.moments(cnt)
                #Extracting Centroid Values
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
                x,y,w,h=cv2.boundingRect(cnt) #x,y coordinates,width,height


                new=True
                if cy in range(up_limit,down_limit):
                    for i in cars:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)

                            if i.going_UP(line_down,line_up)==True:
                                cnt_up+=1
                                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                                cv2.imwrite("./detected_vehicles/vehicleUP" + str(cnt_up) + ".png", img[y:y + h - 1, x:x+w])
                                
                                

                            elif i.going_DOWN(line_down,line_up)==True:
                                cnt_down+=1
                                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                                cv2.imwrite("./detected_vehicles/vehicleDOWN" + str(cnt_down) + ".png", img[y:y + h - 1, x:x+w])
                                

                            break
                        if i.getState()=='1':
                            if i.getDir()=='down'and i.getY()>down_limit:
                                i.setDone()
                            elif i.getDir()=='up'and i.getY()<up_limit:
                                i.setDone()
                        if i.timedOut():
                            index=cars.index(i)
                            cars.pop(index)
                            del i

                    if new==True:
                        p=vehicles.Car(pid,cx,cy,max_p_age)
                        cars.append(p)
                        pid+1
                #cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 2)
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                




        for i in cars:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, (255,255,0), 1, cv2.LINE_AA)
            if line_down+20<= i.getY() <= line_up-20:
               a = (h + (.74*w)- 100)

               if a >= 0:
                     cv2.putText(frame, "Truck", (i.getX(), i.getY()), font, 1, (0,255,255), 2, cv2.LINE_AA)
               else:
                     cv2.putText(frame, "car", (i.getX(), i.getY()), font, 1, (0,0,255), 2, cv2.LINE_AA)


        str_up='UP: '+str(cnt_up)
        str_down='DOWN: '+str(cnt_down)
        
        #To display the Lines
        frame=cv2.line(frame,(0,line_up),(900,line_up),(255,0,255),3,8) #Magenta
        frame=cv2.line(frame,(0,up_limit),(900,up_limit),(0,255,255),3,8) #Cyan
        frame=cv2.line(frame,(0,down_limit),(900,down_limit),(255,0,0),3,8) #Yellow
        frame = cv2.line(frame, (0, line_down), (900, line_down), (255, 0,0), 3, 8) #Blue

        #To display the Texts
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Frame',frame)

        if cv2.waitKey(1)&0xff==ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
