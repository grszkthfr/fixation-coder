#!/usr/bin/python
# by Jonas Großekathöfer, 2019
"""
Module doctring
TODO: PyLint improvements
"""
from os import path
import os
import csv
import cv2
import numpy as np



def getInformaiton(data_dir):

    for i in os.listdir(data_dir):
        subject_id = i
        file_path = path.join(data_dir, subject_id)
        file_path = path.abspath(file_path)

        files_id = '_'.join(str.split(os.listdir(file_path)[1], '_')[:-2])
        print(files_id)

        # output directory
        out_dir = path.join('log_fixations', subject_id)
        out_dir = path.abspath(out_dir)

        # check if file and folder already exist
        if not path.isdir(out_dir):
            os.makedirs(out_dir)  # throws an error when failing


        for part in [1,2]:


            # get file names of validation

            val_before_id = 'val_1_' + str(part)
            print(val_before_id)
            val_after_id = 'val_2_' + str(part)

            val_before_file_name = '_'.join((files_id, val_before_id)) + ".txt"
            val_after_file_name = '_'.join((files_id, val_after_id)) + ".txt"

            val_files = [
                path.join(file_path, val_before_file_name),
                path.join(file_path, val_after_file_name)]

            val_files[0] = path.abspath(val_files[0])
            val_files[1] = path.abspath(val_files[1])

            val_dirs = [
                path.join('log', subject_id, 'frames', val_before_id),
                path.join('log', subject_id, 'frames', val_after_id)]

            val_dirs[0] = path.abspath(val_dirs[0])
            val_dirs[1] = path.abspath(val_dirs[1])

            correctDrift(val_files, val_dirs, out_dir)

def onlyScreenshotFrames(ALL_FRAMES):

    screenshot_frames = []
    for row in ALL_FRAMES[1:]:      # except header
        if (int(row[3]) % 10 == 0 and int(row[3]) >= 230):

            # print(row)
            screenshot_frames.append(row)

    # print(screenshot_frames)
    return(screenshot_frames)

def readFrames(LOG_FILE):

    with open(LOG_FILE, 'r') as f:

        READER = csv.reader(f, delimiter='\t')
        all_frames = list(READER)
        frames = onlyScreenshotFrames(all_frames)
        # print(frames[:5])

    return(frames)

def correctDrift(validation_files, validation_directories, out_dir):
    '''
    Find Val_X_1 and VA_X_2 and compute drift correction
    '''
    val_log = []

    for file in range(len(validation_files)):
        val_log = []
        frames = readFrames(validation_files[file])
        #print(frames[:5])

        frame_dir = validation_directories[file]
        print(frame_dir)

        for i in range(len(frames)):
            frame = frames[i]

            subject_id = frame[0]

            video_id = frame[2]
            frame_id = frame[3]
            #print("THIS IS VALIDATION FRAME ID:", frame_id)

            out_file = path.join(
                out_dir, subject_id + '_' + video_id + '.csv')
            # print(out_file)

            frame_screenshot = video_id + '_' + 'frame_' + frame_id + '.ppm'
            #print('current validation frame:\t\t', frame_screenshot)
            frame_screenshot = path.join(frame_dir, frame_screenshot)
            frame_screenshot = path.abspath(frame_screenshot)
            #print('current validation frame:\t\t', frame_screenshot)

            img = cv2.imread(frame_screenshot)

            gaze_position = (int(float(frame[4])/2), int(float(frame[5])/2))

            gaze_x = gaze_position[0]
            gaze_y = gaze_position[1]

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            sensitivity = 100
            lower_white = np.array([0,0,255-sensitivity])
            upper_white = np.array([255,sensitivity,255])

            # Threshold the HSV image to get only white colors
            mask = cv2.inRange(hsv, lower_white, upper_white)
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(img,img, mask= mask)

            # finding contours
            #ret, thresh = cv2.threshold(mask,127,255,0)
            contours, hierarchy = cv2.findContours(
                mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            for c in contours:
                # compute the center of the contour
                M = cv2.moments(c)
                if M['m00'] > 0:
                    control_x = int(M["m10"] / M["m00"])
                    control_y = int(M["m01"] / M["m00"])
                    cv2.circle(res, (control_x, control_y), 1, (0,255,0), -1)

                    # from: https://2.bp.blogspot.com/-mexnuZ06I-k/Vg1bGIwo_zI/AAAAAAAADZU/oIi52uuKY3Q/s1600/day17-1.JPG
                    distance = np.sqrt((control_x - gaze_x)**2+(control_y - gaze_y)**2)
                    #print('current validation frame:\t\t', frame_screenshot, "\n", distance)

                    val_log.append([subject_id, video_id, frame_id, gaze_x, gaze_y, control_x, control_y, distance])

            # # draw contour
            # cv2.drawContours(res, contours, -1, (0,255,0), 3)

            # # show
            # cv2.imshow('frame', img)
            # #cv2.imshow('thresh', thresh)

            # cv2.imshow('mask', mask)
            # cv2.imshow('res', res)
            # k = cv2.waitKey(3000) & 0xFF

            # if k == 27:
            #     break
            
        out_file = path.join(out_dir, subject_id + '_' + video_id + '.csv')
        # print(out_file)

        with open(out_file, 'a', newline='') as save_file:
            writer = csv.writer(save_file, delimiter='\t')  # tab separated
            if os.stat(out_file).st_size == 0:  # if file is empty, insert header
                writer.writerow((
                    'subject_id', 'video_id', 'frame_id', 'gaze_x', 'gaze_y',
                    'control_x', 'control_y', 'distance'))

            writer.writerows(val_log)


getInformaiton("log")