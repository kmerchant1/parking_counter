import cv2
import pickle



width, height = 107, 48

#we want to save these positions, so we use the pickle library to 'dump' the parking space positions into a file called park_space_positions
#if there is a file that was already created, then we just initialize the positions_list as empty
try:
    with open('park_space_positions', 'rb') as f:
        position_list = pickle.load(f)
except:
    position_list = []

def mouse_click(event, x, y, flags, extra):
    '''
    Defines mouse click event when adding rectangles to all the parking spots
    
    '''
    
    #if we left click, it adds a rectangle with points and color specified below
    if event==cv2.EVENT_LBUTTONDOWN:
        position_list.append((x,y))
    #if we right click, it checks if we clicked inside another rectangle, if so, we delete that rectangle
    if event == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(position_list):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height: 
                position_list.pop(i)
    with open('park_space_positions', 'wb') as f:
        pickle.dump(position_list, f)

while True:
    image = cv2.imread('data/carParkImg.png')
    for pos in position_list:
        cv2.rectangle(image, pos, (pos[0]+width, pos[1]+height), (255,0,255),2)
    
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', mouse_click)
    cv2.waitKey(1)