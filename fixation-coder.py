#!/usr/bin/python

# import sys
# import os
import csv
import cv2
# import math
# import numpy as np

# directories
# LOG_FILE = "subject_01/log_2019-01-09_" + sys.argv[1] + ".txt"
LOG_FILE = "log/subject_01/log_2019-01-25_01_1.9_1.txt"
# FRAME_DIR = "subject_01/frames/" + sys.argv[1] + "/"
FRAME_DIR = "log/subject_01/frames/1.9_1/"  
OUT_DIR = "data/subject_01/"

with open(LOG_FILE, 'r') as f:
    READER = csv.reader(f, delimiter='\t')
    ALL_FRAMES = list(READER)
    # print(ALL_FRAMES[:2])
    for row in ALL_FRAMES[1:]:
        if (int(row[3]) % 10 == 0 and int(row[3]) >= 230):
            # print(row)
            print(row[3] + ".ppm\n" + row[4] + "," + row[5])
            frame = FRAME_DIR + row[2] + "_" + "frame_" + row[3] + ".ppm"
            print(frame)
            img = cv2.imread(frame)

            screenPos = (int(float(row[4])/2), int(float(row[5])/2))  # 216

            cv2.circle(img, screenPos, 1, (0, 255, 255), 4)

            img = cv2.flip(img, 0)  # 0 = horizontal, 1 = vertical, -1 = both

            while 1:
                cv2.imshow("window", img)

                k = cv2.waitKey(33)
                if k == 27:    # Esc key to stop
                    break
                elif k == -1:  # normally -1 returned,so don't print it
                    continue
                else:
                    print(repr(chr(k % 256)))
                    break  # else print its value
