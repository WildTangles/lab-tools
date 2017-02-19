import cv2
import numpy as np
import pickle
import csv

file_select = raw_input("give me food\n")
#file_select = 'h3s2.mov'
cap = cv2.VideoCapture(file_select)
previousMassVal = 10.0 #211 for h2s2 210 for rest
aD = 0.2
tC = 0
#cap = cv2.VideoCapture('heatedrun3session2.MOV')

ix, iy = -1, -1
threshold = 130 #150 for h3s2 180 for rest
checkThreshold = False

cv2.namedWindow('frame')
# pkl_output_filex = open(file_select+'x', 'rb')
# pkl_output_filey = open(file_select+'y', 'rb')
# locksx = pickle.load(pkl_output_filex)
# locksy = pickle.load(pkl_output_filey)
pkl_output_file = open(file_select+'index_voltage', 'rb')
locks = pickle.load(pkl_output_file)
digits = [locks[i:i+7] for i in range(0, len(locks), 7)]
print digits
print len(digits)
one = [0,1,0,0,1,0,0]
two = [1,1,0,1,0,1,1]
three = [1,1,0,1,1,0,1]
four = [0,1,1,1,1,0,0]
five = [1,0,1,1,1,0,1]
six = [1,0,1,1,1,1,1]
seven = [1,1,0,0,1,0,0]
eight = [1,1,1,1,1,1,1]
nine = [1,1,1,1,1,0,1]
zero = [1,1,1,0,1,1,1]
mass = []
masscheck = []
masscheck.append(previousMassVal)
#oldreading = 0
while cap.isOpened():

    ret, frame = cap.read()


    count = 0
    toPrint = True
    reading = []
    for digit in digits:
        identity = []
        for lock in digit:
            pixel = frame[lock[1], lock[0]]
            checksum = ((int(pixel[0])) + (int(pixel[1])))/2.0
            if checksum <= threshold:
                if checkThreshold:
                    print 'inside'
                identity.append(1)
            else:
                identity.append(0)
        if np.array_equal(identity, one):
            reading.append(1)
        elif np.array_equal(identity, two):
            reading.append(2)
        elif np.array_equal(identity, three):
            reading.append(3)
        elif np.array_equal(identity, four):
            reading.append(4)
        elif np.array_equal(identity, five):
            reading.append(5)
        elif np.array_equal(identity, six):
            reading.append(6)
        elif np.array_equal(identity, seven):
            reading.append(7)
        elif np.array_equal(identity, eight):
            reading.append(8)
        elif np.array_equal(identity, nine):
            reading.append(9)
        elif np.array_equal(identity, zero):
            reading.append(0)
        else:
            #reading.append(oldreading-1)
            #print identity
            #print "AAAAAAAAAAAAAAAA"
            toPrint = False
            #break

    if toPrint:
        #massVal = reading[0] * 100.0 + reading[1] * 10.0 + reading[2] + (reading[3]/10.0)
        massVal = reading[0] + reading[1]/10.0 + reading[2]/100.0
        if previousMassVal - massVal < aD or tC > 3:
            tC = 0
            #if massVal <= min(masscheck):
            if True:
                mass.append((massVal, (cap.get(0)/1000.0)))
                masscheck.append(massVal)
                #print str(massVal) + "@" + str(cap.get(0)/1000.0)
                print mass[-1]
                fd = open(file_select + 'VOLTAGE.csv','ab')
                fd.write(str(cap.get(0)/1000.0) + ',' + str(massVal) + '\n')
                fd.close()
            previousMassVal = massVal
        else:
            tC += 1


    # #oldreading = reading[0]
    # if toPrint:
    #     print reading[3]

    cv2.imshow('frame', frame)
    k = 0xFF & cv2.waitKey(1)
    #cv2.waitKey(20) &
    if k == 27:
        break
    elif k == ord('s'):
        break
print mass
cap.release()
cv2.destroyAllWindows()