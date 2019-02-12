#!/usr/bin/python

import sys
from os import path
import os
import csv
import cv2

# #APP
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog,QLineEdit, QMenu # QPushButton, QLineEdit

# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# from PyQt5.QtGui import QIcon, QPixmap

#############################################################################
################# Settings  #################################################
#############################################################################

# log file
LOG_FILE = "log_2019-01-25_01_val_1_1.txt"

# keys
key_fix_person = 49         # key "1" to code a fixation_id on a person 
key_fix_object = 50         # key "2" to code a fixation_id on a object
key_fix_person_absent = 51  # key "3" to code a fixation_id w/o person in scene
key_no_fixation = 48        # key "0" to code a fixation_id on a person
key_delete_frame = 100    # key "d" to delete previuos line, go to previous frame
key_next_frame = 32         # key "space" to write line, go to next frame
key_exit = 27

#############################################################################



def writeLine(out_file, subject_id, video_id, frame_id, fixation_id):

    fixation_dummy = fixationDummyCoding(fixation_id)

    # generate file name with name of the experiment and subject
    # open file
    # 'a' = append; 'w' = writing; 'b' = in binary mode
    with open(out_file, 'a',newline='') as save_file:
        writer = csv.writer(save_file, delimiter='\t') # tab separated
        if os.stat(out_file).st_size == 0:  # if file is empty, insert header
            writer.writerow(("subject_id", "video_id", "frame_id", "fixation_id", "fix_person", "fix_object", "fix_person_absent", "no_fixation"))

        # write trial
        print("WRITE (regular):\n", [int(str.split(subject_id, "_")[1]), video_id, frame_id, fixation_id, fixation_dummy[0], fixation_dummy[1], fixation_dummy[2], fixation_dummy[3]])
        writer.writerow([int(str.split(subject_id, "_")[1]), video_id, frame_id, fixation_id, fixation_dummy[0], fixation_dummy[1], fixation_dummy[2], fixation_dummy[3]])

    save_file.close() # needed? to safely delete rows

def deleteLine(out_file):

    with open(out_file, 'r') as save_file:
        
        reader = csv.reader(save_file, delimiter='\t')

        new_save_file = list(reader)
        #print("OLD:\n", new_save_file)
        #print("DELETE:\n", new_save_file[-1]) # deleted
        new_save_file = new_save_file[:-1] # truncat last entry
        #print("NEW:\n", new_save_file)

    # write trials, without deleted one
    with open(out_file, 'w', newline='') as save_file:
        writer = csv.writer(save_file, delimiter='\t') # tab separated

        #print("WRITE (deleted):\n", [row for row in new_save_file])
        for row in new_save_file:
            writer.writerow(row)



    # with open(out_file, 'w',newline='') as save_file:
    #     writer = csv.writer(save_file, delimiter='\t') # tab separated
    #     writer.writerow((lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6], lines[7]))

        #out_file.close()
        #writer = csv.writer(new_save_file, delimiter='\t') # tab separated
        #writer.writerows(new_save_file)


def fixationDummyCoding(fixation_id):

    if fixation_id == "person":
        fixation_dummy = [1,0,0,0]

    elif fixation_id == "object":
        fixation_dummy = [0,1,0,0]

    elif fixation_id == "person_absent":
        fixation_dummy = [0,0,1,0]

    elif fixation_id == "no_fixation":
        fixation_dummy = [0,0,0,1]

    elif fixation_id == "unkown":
        fixation_dummy =[0,0,0,0]

    else:
        fixation_dummy = ["","","",""]

    return(fixation_dummy)

def readFrames(LOG_FILE):

    with open(LOG_FILE, 'r') as f:

        READER = csv.reader(f, delimiter='\t')
        all_frames = list(READER)
        frames = onlyScreenshotFrames(all_frames)
        #print(frames[:5])

    return(frames)

def onlyScreenshotFrames(ALL_FRAMES):

    screenshot_frames = []
    for row in ALL_FRAMES[1:]:      # except header
        if (int(row[3]) % 10 == 0 and int(row[3]) >= 230):

            #print(row)
            screenshot_frames.append(row)

    #print(screenshot_frames)
    return(screenshot_frames)

# def showScreenshotWithFixation(FRAME):

#def handleInput(NEXT_FRAME):


def drawFixation(log_file, frame_directory="frames"):

    # extract relevant information from log filename
    subject_id = "subject_" + str.split(log_file, "_")[2]
    video_id = log_file[18:-4]
    log_file = path.join("log", subject_id, log_file)
    log_file = path.abspath(log_file)

    # directory of frames
    frame_dir = path.join("log", subject_id, "frames", video_id)
    frame_dir = path.abspath(frame_dir)

    # output directory
    out_dir = path.join("log_fixations", subject_id)
    out_dir = path.abspath(out_dir)
        # check if file and folder already exist
    if not path.isdir(out_dir):
        os.makedirs(out_dir) # throws an error when failing

    out_file = path.join(out_dir, str.split(subject_id, "_")[1] + '-' + video_id + '.csv')
    #print(log_fixations_name)

    frames = readFrames(log_file)
    #print(frames[:5])

    counter = 0
    while counter <= len(frames): 

        # print(frame[3] + ".ppm\n" + frame[4] + "," + frame[5])
        frame = frames[counter]

        video_id = frame[2]
        frame_id = frame[3]

        frame_screenshot = video_id + "_" + "frame_" + frame_id + ".ppm"
        #print(frame_screenshot)
        frame_screenshot = path.join(frame_dir, frame_screenshot)
        frame_screenshot = path.abspath(frame_screenshot)

        img = cv2.imread(frame_screenshot)

        screenPos = (int(float(frame[4])/2), int(float(frame[5])/2))  # 216

        cv2.circle(img, screenPos, 3, (0, 255, 255), 2)


        img = cv2.flip(img, 0)  # 0 = horizontal, 1 = vertical, -1 = both
        cv2.putText(img, frame_id, (200,200), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        cv2.imshow("frame", img)

        #return(img)

        next_frame = True
        while next_frame:

            cv2.imshow("frame", img)

            k = cv2.waitKey(33)

            if k == key_exit:  # Esc
                next_frame = False
                break

            elif k == -1:  # normally -1 returned, so don't print it
                continue

            elif k == key_fix_person:  # #1
                fixation_id = "person"
                #break

            elif k == key_fix_object:  # #2
                fixation_id = "object"
                #break

            elif k == key_fix_person_absent:  # #2
                fixation_id = "person_absent"
                #break

            elif k == key_no_fixation:  # #2
                fixation_id = "no_fixation"
                #break

            elif k == key_delete_frame: # d
                fixation_id = "deleted"
                #deleteLine(out_file)
                # int(frame_id) -= 10
                #counter -= 2 # because space adds 1
                #break

            elif k == key_next_frame: # space

                #if fixation_id == "unkown"
                if fixation_id != "deleted":
                    counter +=1
                    writeLine(out_file, subject_id, video_id, frame_id, fixation_id) # write line into file

                elif fixation_id == "deleted":
                    counter -= 1
                    deleteLine(out_file)

                break

            else: # else print its value
                fixation_id = "unknown"
                print(k)
                # print(repr(chr(k % 256))) # https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv
                #break

        print(fixation_id)
        fixation_id = "unknown"

        if next_frame == False: break

# def setup():

#     app = QApplication(sys.argv)
#     win = QWidget()

#     # textbox for log file name
#     textbox = QLineEdit(win)
#     textbox.setDragEnabled(True)
#     textbox.setText("log_2019-01-25_01_1.9_1.txt")
#     textbox.setToolTip(
#         "Please enter exact file name of log file")
#     textbox.move(100, 100)
#     textbox.resize(280, 40)

#     # start button
#     button = QPushButton(win)
#     button.setText("Start")
#     button.move(50, 50)
#     button.clicked.connect(start_coding)

#     win.setWindowTitle("Fixation Coder App")
#     win.show()
#     sys.exit(app.exec_())


# def start_coding():

#     drawFixation(LOG_FILE)


# setup()

drawFixation(LOG_FILE)