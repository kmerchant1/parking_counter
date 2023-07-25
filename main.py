import pickle
import cvzone
import cv2
import numpy as np

#1hr Video Feed

cap = cv2.VideoCapture('data/carPark.mp4')
width, height = 107, 48

#We dont have to wrap in 'try' block because we know there will be a file for sure
with open('park_space_positions', 'rb') as f:
        position_list = pickle.load(f)

def draw_rect_full(pos):
        cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height), (0,0,255),thickness=2)
def draw_rect_empty(pos):
        cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height), (124,252,0),2)

def check_space(frame_processed):
    free_spaces = 0
    
    #draw rectangle positions from our selector file
    for pos in position_list:
        x,y = pos
        
        
        #create a new 'image' for each parking space which we will then use to check if the space is empty
        space = frame_processed[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), space)       this was for testing if the new image was accurately showing the parking space
        
        #count the number of empty pixels to determine whether there is a car or not
        #this means that if the 'count' is very low, then we can classify the space as empty....otherwise it is occupied
        count = cv2.countNonZero(space)
        cvzone.putTextRect(frame, str(count), (x,y+height-5), scale=1.5, thickness=2, offset=0)
        if count>850:
            draw_rect_full(pos)         
        else:
            draw_rect_empty(pos)
            free_spaces+=1
        
        cvzone.putTextRect(frame, f'{free_spaces}/{len(position_list)}', (300,50), scale=4, thickness=2, colorR=(124,252,0))

while cap.isOpened:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    
    success, frame = cap.read()
    #convert to gray scale so we can check if car is in the parking space
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_scale, (3,3), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                   25,16)
    frame_median = cv2.medianBlur(thresh, 5)
    kernel = np.ones((3,3),np.uint8)
    frame_dilate = cv2.dilate(frame_median, kernel, iterations=1)
    
    
    check_space(frame_dilate)
        
    #render video feed
    cv2.imshow('Video Feed', frame)
    # cv2.imshow('Blur', blur)
    # cv2.imshow('Threshold', thresh)
    
    
    
    
    
    
    
    
    
    if cv2.waitKey(25) & 0xFF ==ord('q'):
        break
