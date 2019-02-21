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

#############################################################################
################# Settings  #################################################
#############################################################################

# log file
LOG_FILE = 'log_2019-02-01_17_1.41_2.txt'

# keys
KEY_FIX_PERSON = 49         # key "1" to code a fixation_id on a person
KEY_FIX_OBJECT_MOVING = 50         # key "2" to code a fixation_id on a object
KEY_FIX_OBJECT_STATIC = 51  # key "3" to code a fixation_id w/o person in scene

# key "2" to code a fixation_id on a object
KEY_FIX_OBJECT_MOVING_NP = 119
# key "3" to code a fixation_id w/o person in 
KEY_FIX_OBJECT_STATIC_NP = 101

KEY_NO_FIXATION = 109        # key "0" to code a fixation_id on a person
KEY_DELETE_FRAME = 100      # key "d" to delete previuos frame,. go back
KEY_NEXT_FRAME = 32         # key "space" to write line, go to next frame
KEY_EXIT = 27

#############################################################################


def writeLine(out_file, subject_id, video_id, frame_id, fixation_id):

    fixation_dummy = fixationDummyCoding(fixation_id)

    with open(out_file, 'a', newline='') as save_file:
        writer = csv.writer(save_file, delimiter='\t')  # tab separated
        if os.stat(out_file).st_size == 0:  # if file is empty, insert header
            writer.writerow((
                'subject_id', 'video_id', 'frame_id',
                'fixation_id', 'fix_person', 'fix_object',
                'fix_person_absent', 'no_fixation'))

        # write trial
        # print(
        #     'WRITE (regular):\n',
        #     [int(str.split(subject_id, '_')[1]), video_id, frame_id,
        #     fixation_id, fixation_dummy[0], fixation_dummy[1],
        #     fixation_dummy[2], fixation_dummy[3]])

        # TODO why brackets?
        writer.writerow([
            int(str.split(subject_id, '_')[1]), video_id, frame_id,
            fixation_id, fixation_dummy[0], fixation_dummy[1],
            fixation_dummy[2], fixation_dummy[3]])

    # save_file.close() # needed? to safely delete rows


def deleteLine(out_file):
    """
    Funciton doctring
    """
    with open(out_file, 'r') as save_file:

        reader = csv.reader(save_file, delimiter='\t')

        new_save_file = list(reader)
        # print('OLD:\n', new_save_file)
        # print('DELETE:\n', new_save_file[-1])  # deleted

        new_save_file = new_save_file[:-1]  # truncat last entry
        # print('NEW:\n', new_save_file)

    # write trials, without deleted one
    with open(out_file, 'w', newline='') as save_file:
        writer = csv.writer(save_file, delimiter='\t')  # tab separated

        # print('WRITE (deleted):\n', [row for row in new_save_file])
        for row in new_save_file:
            writer.writerow(row)


def fixationDummyCoding(fixation_id):
    # TODO why brackets?
    if fixation_id == 'person':
        fixation_dummy = [1, 0, 0, 0]

    elif fixation_id == 'object':
        fixation_dummy = [0, 1, 0, 0]

    elif fixation_id == 'person_absent':
        fixation_dummy = [0, 0, 1, 0]

    elif fixation_id == 'no_fixation':
        fixation_dummy = [0, 0, 0, 1]

    elif fixation_id == 'unkown':
        fixation_dummy = [0, 0, 0, 0]

    else:
        fixation_dummy = ['', '', '', '']

    return(fixation_dummy)


def readFrames(LOG_FILE):

    with open(LOG_FILE, 'r') as f:

        READER = csv.reader(f, delimiter='\t')
        all_frames = list(READER)
        frames = onlyScreenshotFrames(all_frames)
        # print(frames[:5])

    return(frames)


def onlyScreenshotFrames(ALL_FRAMES):

    screenshot_frames = []
    for row in ALL_FRAMES[1:]:      # except header
        if (int(row[3]) % 10 == 0 and int(row[3]) >= 230):

            # print(row)
            screenshot_frames.append(row)

    # print(screenshot_frames)
    return(screenshot_frames)


# TODO saving screenshots
def showScreenshotWithFixation(FRAME):
    print("TODO")


# TODO handle keys
def handleInput(NEXT_FRAME):
    print("TODO")


def updateImageInformation(image, frame_id, fixation_id):

    font = cv2.FONT_HERSHEY_PLAIN
    height, width, channels = image.shape

    # frame information box
    cv2.rectangle(
        image,
        (0, height-50), (int(width/1.5), height),
        (0, 0, 0), -1)

    # frame_id
    cv2.putText(
        image,
        'frame_id: ' + frame_id, (0, height-25),
        font, 1, (255, 255, 255))

    # fixtiaon_id
    cv2.putText(
        image,
        'current fixation_id: ' + fixation_id, (0, height-12),
        font, 1, (255, 255, 255))

    # TODO to make rectangle transparent: https://www.pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/
    # apply the overlay
    # cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # update window
    cv2.imshow('frame', image)


def drawFixation(log_file_name, frame_directory='frames'):

    # extract relevant information from log filename
    subject_id = 'subject_' + str.split(log_file_name, '_')[2]
    part_id = 'session_' + str.split(log_file_name, '_')[4][:-4]
    video_id = log_file_name[18:-4]

    # pre stuff for each file in directory start with inclduing log_ date_ subject_id
    files_id = '_'.join(str.split(log_file_name, '_')[:-2])

    path_files = path.join('log', subject_id)
    log_file = path.join(path_files, log_file_name)
    log_file = path.abspath(log_file)

    # # get file names of validation

    # val_before_id = 'val_1_' + str.split(part_id, '_')[1]
    # print(val_before_id)
    # val_after_id = 'val_2_' + str.split(part_id, '_')[1]

    # val_before_file_name = '_'.join((files_id, val_before_id)) + ".txt"
    # val_after_file_name = '_'.join((files_id, val_after_id)) + ".txt"

    # val_files = [
    #     path.join(path_files, val_before_file_name),
    #     path.join(path_files, val_after_file_name)]

    # val_files[0] = path.abspath(val_files[0])
    # val_files[1] = path.abspath(val_files[1])
    
    # val_dirs = [
    #     path.join('log', subject_id, 'frames', val_before_id),
    #     path.join('log', subject_id, 'frames', val_after_id)]

    # val_dirs[0] = path.abspath(val_dirs[0])
    # val_dirs[1] = path.abspath(val_dirs[1])


    # directory of frames
    frame_dir = path.join('log', subject_id, 'frames', video_id)
    frame_dir = path.abspath(frame_dir)



    # output directory
    out_dir = path.join('log_fixations', subject_id)
    out_dir = path.abspath(out_dir)

    # check if file and folder already exist
    if not path.isdir(out_dir):
        os.makedirs(out_dir)  # throws an error when failing

    out_file = path.join(
        out_dir, str.split(subject_id, '_')[1] + '_' + video_id + '.csv')
    # print(out_file)

    #correctDrift(val_files, val_dirs, out_dir)


    frames = readFrames(log_file)
    # print(frames[:5])
    fixation_id = ''

    counter = 0
    while counter < len(frames):

        frame = frames[counter]

        video_id = frame[2]
        frame_id = frame[3]

        frame_screenshot = video_id + '_' + 'frame_' + frame_id + '.ppm'
        print('current frame:\t\t', frame_screenshot)
        frame_screenshot = path.join(frame_dir, frame_screenshot)
        frame_screenshot = path.abspath(frame_screenshot)

        img = cv2.imread(frame_screenshot)

        gaze_position = (int(float(frame[4])/2), int(float(frame[5])/2))  # 216

        cv2.circle(img, gaze_position, 3, (0, 255, 255), 2)

        img = cv2.flip(img, 0)  # 0 = horizontal, 1 = vertical, -1 = both

        updateImageInformation(img, frame_id, fixation_id)

        cv2.imshow('frame', img)

        # return(img)

        next_frame = True
        while next_frame:

            cv2.imshow('frame', img)

            k = cv2.waitKey(33)

            if k == KEY_EXIT:  # Esc

                next_frame = False
                cv2.destroyAllWindows()
                break

            elif k == -1:  # normally -1 returned, so don't print it
                continue

            elif k == KEY_FIX_PERSON:  # #1
                fixation_id = 'person'
                updateImageInformation(img, frame_id, fixation_id)

            elif k == KEY_FIX_OBJECT_MOVING:  # #2
                fixation_id = 'object_moving'
                updateImageInformation(img, frame_id, fixation_id)

            elif k == KEY_FIX_OBJECT_STATIC:  # #3
                fixation_id = 'object_static'
                updateImageInformation(img, frame_id, fixation_id)

            elif k == KEY_FIX_OBJECT_MOVING_NP:  # #2
                fixation_id = 'object_moving_no-person'
                updateImageInformation(img, frame_id, fixation_id)

            elif k == KEY_FIX_OBJECT_STATIC_NP:  # #3
                fixation_id = 'object_static_no-person'
                updateImageInformation(img, frame_id, fixation_id)


            elif k == KEY_NO_FIXATION:  # n
                fixation_id = 'no_fixation'
                updateImageInformation(img, frame_id, fixation_id)

            elif k == KEY_DELETE_FRAME:  # d
                fixation_id = 'deleted'

            # TODO make a "valid_code = TRUE"
            elif k == KEY_NEXT_FRAME and fixation_id != 'unknown' and fixation_id != '':  # space

                if fixation_id != 'deleted':
                    counter += 1
                    writeLine(
                        out_file, subject_id, video_id, frame_id, fixation_id)

                elif fixation_id == 'deleted':
                    counter -= 1
                    deleteLine(out_file)

                break

            else:  # else print key value
                fixation_id = 'unknown'
                print(k)
                # print(repr(chr(k % 256)))  # https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv
                # break

        print('coded fixation_id:\t', fixation_id)

        # fixation_id = 'unknown'

        if next_frame is False:
            break


drawFixation(LOG_FILE)
