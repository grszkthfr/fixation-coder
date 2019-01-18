#!/usr/bin/python

import sys
import os
import csv
import cv2 as cv2
import math
import numpy as np

# directories
#log_file = "pilot_99/log_2019-01-09_" + sys.argv[1] + ".txt"
log_file = "pilot_99/log_2019-01-17_99_val_black_1_1.txt"
#frame_dir = "pilot_99/frames/" + sys.argv[1] + "/"
frame_dir = "pilot_99/frames/val_black_1_1/"  
out_dir = "pilot_99/data/"

# # window full screen
# cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

all_x = []
all_y = []

with open(log_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    all_frames = list(reader)
    #print(all_frames[:2])
    for row in all_frames[1:]:
        if (int(row[3]) % 6 == 0 and int(row[3]) > 227): 
        # for real data when every 10th frame: if (int(row[3]) % 10 == 0 and int(row[3]) >= 230): #and (row[4] != "0" and row[5] != "0"): # ignoring first 5 seconds of vid
            #print(row)
            print(row[3] + ".ppm\n" + row[4] + "," + row[5])
            frame = frame_dir + "frame_" + row[3] + ".ppm"
            print(frame)
            img = cv2.imread(frame)
                    
            screenPos = (int(float(row[4])/2), int(float(row[5])/2)) # 216
            

            # ## WIP: color detection; try to find gaze by smi
            # lower = np.array([7,71,90], dtype = "uint8")
            # upper = np.array([10,75,100], dtype = "uint8")
            # mask = cv2.inRange(img, lower, upper)
            # roi = cv2.bitwise_and(img, img, mask=mask)
            # roi_gry = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # ret, thresh = cv2.threshold(roi_gry, 127, 255, 0)
            # roi_gry2, contours, hierachy = cv2.findContours(thresh, 1, 2)
            # cnt = sorted(contours, key=cv2.contourArea, reverse=True)
            # print(cnt)

            # if len(cnt) != 0:
            #     print(len(cnt))
            #     gbs_x1, gbs_y1, gbs_w, gbs_h = cv2.boundingRect(cnt[0])
                
            #     gbs_x2 = gbs_x1 + gbs_w
            #     gbs_y2 = gbs_y1 + gbs_h
            #     cv2.rectangle(img, (gbs_x1, gbs_y1), (gbs_x2, gbs_y2), (172,15,15),3)

            # else:
            #     cv2.putText(img,"collor detection failed", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3)

            cv2.circle(img, screenPos, 1, (0,255,255), 4)
            
            # dist = int(round(math.sqrt((screenPos[0]-960)**2 + (screenPos[0]-540)**2)))


            # cv2.circle(img, (int(float(row[5])), int(float(row[6]))), 15, (255,255,255), 3)

            img = cv2.flip(img,0) # 0 = horizontal, 1 = vertical, -1 = both
            # cv2.putText(img,str(dist) + " | (" + row[5] + ", " + row[6] + ")", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3)

            all_x.append(screenPos[0])
            all_y.append(screenPos[1])

            # print(min(all_x))
            # print(max(all_x))
            # print(min(all_y))
            # print(max(all_y))

            sml_img = cv2.resize(img, (0,0), fx=1, fy=1)

            while(1):
                cv2.imshow('window', sml_img)

                k = cv2.waitKey(33)
                if k==27:    # Esc key to stop
                    break
                elif k==-1:  # normally -1 returned,so don't print it
                    continue
                else:
                    print(repr(chr(k%256)))
                    break # else print its value
            #cv2.imwrite(out_dir + frame + ".png", img)

            #cv2.imshow('image', sml_img[::-1])
            # cv2.waitKey()
            

#         cv2.destroyAllWindows()


# print(min(all_x))
# print(max(all_x))
# print(min(all_y))
# print(max(all_y))
#        #
        # #cv2.imwrite(out_dir + frame + ".png", img)