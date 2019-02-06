#!/usr/bin/python

import sys
from os import path
import csv
import cv2
# import math
# import numpy as np

#APP
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog,QLineEdit, QMenu # QPushButton, QLineEdit

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

LOG_FILE = "log_2019-01-25_01_val_1_1.txt"

# OUT_DIR = "data/subject_01/"

def write_line(OUTPUT_DIR, INPUT):

    # check if file and folder already exist
    makeDirectory('log_files')
    fileName = 'log_files' + os.path.sep + exp_name + '_' + getDate() + '_' + session_info['subject'].zfill(2) + '.csv' 

    # generate file name with name of the experiment and subject
    # open file
    # 'a' = append; 'w' = writing; 'b' = in binary mode
    with open(fileName, 'ab') as saveFile:
        fileWriter = csv.writer(saveFile, delimiter='\t') # tab separated
        if os.stat(fileName).st_size == 0:  # if file is empty, insert header
            fileWriter.writerow(('INPUT'))

        # write trial
        fileWriter.writerow(INPUT)


def draw_fixation():
    print("Draw Fixation from log of frame into img of frame")


def get_frames_img():
    print("Handled img of frame")


def get_frames_log(log_file):
    print("Handled log of frame")


def load_log(log_file):
    print("Loaded log file")


def drawFixation(log_file, frame_directory = "frames"):

    # extract relevant information from log filename
    SUBJECT_ID = "subject_" + str.split(log_file, "_")[2]
    VIDEO_ID = log_file[18:-4]
    LOG_FILE = path.join("log", SUBJECT_ID, log_file)
    LOG_FILE = path.abspath(LOG_FILE)

    # directory of frames
    FRAME_DIR = path.join("log", SUBJECT_ID, "frames", VIDEO_ID)
    FRAME_DIR = path.abspath(FRAME_DIR)

    with open(LOG_FILE, 'r') as f:

        READER = csv.reader(f, delimiter='\t')
        ALL_FRAMES = list(READER)

        # print(ALL_FRAMES[:2])
        for row in ALL_FRAMES[1:]:      # except header

            if (int(row[3]) % 10 == 0 and int(row[3]) >= 230):

                # print(row[3] + ".ppm\n" + row[4] + "," + row[5])

                FRAME_FILE = row[2] + "_" + "frame_" + row[3] + ".ppm"
                FRAME = path.join(FRAME_DIR, FRAME_FILE)

                img = cv2.imread(FRAME)

                screenPos = (int(float(row[4])/2), int(float(row[5])/2))  # 216

                cv2.circle(img, screenPos, 3, (0, 255, 255), 2)

                img = cv2.flip(img, 0)  # 0 = horizontal, 1 = vertical, -1 = both

                #cv2.imshow("frame", img)

                return(img)

                next_frame = True
                while next_frame:

                    cv2.imshow("frame", img)

                    k = cv2.waitKey(33)

                    if k == 27:    # Esc key to stop
                        next_frame = False
                        break

                    elif k == -1:  # normally -1 returned, so don't print it
                        continue

                    elif k == 49: # #1
                        fixation = "person"
                        break

                    elif k == 50:  # #2
                        fixation = "object"
                        break

                    else:
                        print(repr(chr(k % 256)))
                        print()
                        break  # else print its value

                print(fixation)
                if next_frame == False: break
                

# def window():
#     app = QApplication(sys.argv)
#     win = QWidget()
#     button = QPushButton(win)
#     button.setText("Hello World!")
#     button.move(50, 50)
#     button.clicked.connect(showimg)

#     # textbox
#     textbox = QLineEdit(win)
#     textbox.setDragEnabled(True)
#     textbox.setText("subject_")
#     textbox.setToolTip(
#         "Please enter subject id. Don't forget trailing 0 for id's < 9")
#     textbox.move(20, 20)
#     textbox.resize(280, 40)

#     # # dropdown
#     # menu = QMenu()
    
#     # # sub_menu = QMenu("Sub Menu")
#     # # for i in ["a", "b", "c"]: #or your dict
#     # #     sub_menu.addAction(i) #it is just a regular QMenu

#     # win.addMenu(sub_menu)

#     win.setWindowTitle("Fixation Coder App")
#     win.show()
#     sys.exit(app.exec_())

# def showimg():
#     app = QApplication(sys.argv)
#     win = QWidget()
#     #setWindowTitle("Frame")
#     #setGeometry(self.left, self.top, self.width, self.height)
      
#     # Create widget
#     label = QLabel()
#     pixmap = QPixmap('log//subject_01//frames//val_1_1//val_1_1_frame_00370.ppm')
#     label.setPixmap(pixmap)
#     win.resize(pixmap.width(),pixmap.height())
      
#     win.show()
#     #sys.exit(app.exec_())


# # Create textbox
# self.textbox = QLineEdit(self)
# self.textbox.move(20, 20)
# self.textbox.resize(280,40)

# # Create a button in the window
# self.button = QPushButton('Show text', self)
# self.button.move(20,80)

# # connect button to function on_click
# self.button.clicked.connect(self.on_click)
# self.show()

#window()
#drawFixation(log_file=LOG_FILE)


# drawFixation(LOG_FILE, FRAME_DIR)
