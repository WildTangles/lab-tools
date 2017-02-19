#DELETE OLD INDEX FILE BEFORE USING THIS
import cv2
import numpy as np
import pickle

file_select = raw_input("give me food\n")
#file_select = 'h3s2.mov'
cap = cv2.VideoCapture(file_select)
#cap = cv2.VideoCapture('heatedrun3session2.MOV')

ix, iy = -1, -1
locks = []
#locksx, locksy = [], []
# mouse callback function
def mouse_click(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
        ix,iy = x,y

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_click)
while cap.isOpened():

    ret, frame = cap.read()

    img = np.zeros((512,512,3), np.uint8)
    cv2.circle(img, (3,4), 200, (0,0,255), -1)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    elif k == ord('s'):
        break
    elif k == ord('a'):
        locks.append((ix, iy))
        # locksx.append(ix)
        # locksy.append(iy)
        print ix, iy
        print frame[iy, ix]
    elif k == ord('b'):
        # pkl_input_filex = open(file_select + 'x', 'wb')
        # pkl_input_filey = open(file_select + 'y', 'wb')
        # pickle.dump(locksx, pkl_input_filex)
        # pickle.dump(locksy, pkl_input_filey)
        # pkl_input_filex.close()
        # pkl_input_filey.close()
        if len([locks[i:i+7] for i in range(0, len(locks), 7)]) != 4:
            print 'something is wrong ...'
            print len([locks[i:i+7] for i in range(0, len(locks), 7)])
        else:
            pkl_input_file = open(file_select + 'index', 'wb')
            pickle.dump(locks, pkl_input_file)
            pkl_input_file.close()
        break

cap.release()
cv2.destroyAllWindows()