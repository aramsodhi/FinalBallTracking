#Import Statments
import cv2 
import numpy as np
import math
from networktables import NetworkTables

# Network tables
NetworkTables.initialize(server="10.29.84.141")
sd = NetworkTables.getTable("SmartDashboard")

#make mask
target_color = sd.getValue("alliance_color") #2 is red & 1 is blue
if (target_color == 2): #red
    red_lower_1 = np.array([0, 100, 20])
    red_upper_1 = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100,20])
    red_upper_2 = np.array([179, 255, 255])
    def make_mask(hsv_frame):
        return cv2.bitwise_or(cv2.inRange(hsv_frame, red_lower_1, red_upper_1), cv2.inRange(hsv_frame, red_lower_2, red_upper_2))
        
elif(target_color == 1):
    blue_lower_1 = np.array([90, 100, 20])
    blue_upper_1 = np.array([130, 255, 255])

    def make_mask(hsv_frame):
        return cv2.inrange(hsv_frame, blue_lower_1, blue_upper_1)

#capture video
cap = cv2.VideoCapture(0)
h_resolution = 320
v_resolution = 240
cap.set(3,h_resolution)
cap.set(4,v_resolution)

h_fov = 50

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(True):
    ret, frame = cap.read()
    
    frame = cv2.GaussianBlur(frame, (7,7),cv2.BORDER_DEFAULT)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = make_mask(hsv_frame)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    frame = cv2.bitwise_and(mask,frame)
    
    circles = cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT_ALT,4,15,param1=300,param2=0.95,minRadius=0,maxRadius=-1) 
    
    if circles is not None:
        
        #print("ball found")
        sd.putValue("ball_on_screen", True)
        sd.putValue("ball_x", circles[0][0][0])
        sd.putValue("ball_y", circles[0][0][1])
        sd.putValue("angle", (180/math.pi)*(math.atan([((circles[0][0][0]-160)*distance)/323.5]/distance))) #I have a way to get the true angle if anyone wants it - Henri
        sd.putValue("distance", (4.75*323.5)/circles[0][0][2])
    
    else:
        #print("no ball found")
        sd.putValue("ball_on_screen", False)
        sd.putValue("ball_x", 0)
        sd.putValue("ball_y", 0)
        sd.putValue("angle", 0)
        sd.putValue("distance", 0)

    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()