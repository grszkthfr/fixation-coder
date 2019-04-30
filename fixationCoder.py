#!/usr/bin/python
# by Jonas Großekathöfer, 2019
"""
Just good enough script to code fixations for each subject for each recorded
frame.
To code any subject or video, please specifiy the according log below in the
settings section and have fun coding. :-)
"""
from os import path
import os
import csv
import cv2
import numpy as np
import itertools

#############################################################################
################# Settings  #################################################
#############################################################################

# log file
LOG_FILE = 'PUT_LOG_FILENAME_HERE.txt'

# keys
KEY_FIX_PERSON = 49         # key "1" to code a fixation_id on a person
KEY_FIX_OBJECT_MOVING = 50  # key "2" to code a fixation_id on a object
KEY_FIX_OBJECT_STATIC = 51  # key "3" to code a fixation_id w/o person in scene
KEY_FIX_BACKGROUND = 52     # key "4"

KEY_PERSON_IN_SCENE = 112   # key "p"

KEY_NO_FIXATION = 110       # key "0" to code a fixation_id on a person
KEY_DELETE_FRAME = 100      # key "d" to delete previuos frame,. go back
KEY_NEXT_FRAME = 32         # key "space" to write line, go to next frame
KEY_EXIT = 27

#############################################################################

def here(file_name=".here"):

    """
    from: https://stackoverflow.com/questions/37427683/python-search-for-a-file-in-current-directory-and-all-its-parents
    adapted to work with here-package in R
    """

    current_dir = os.getcwd()  # search starts here
    # print(current_dir)

    while True:
        file_list = os.listdir(current_dir)
        parent_dir = os.path.dirname(current_dir)
        if file_name in file_list:
            # print("File Exists in: ", current_dir)
            break

        else:
            if current_dir == parent_dir:  # if dir is root dir
                # print("File not found")
                break
            else:
                current_dir = parent_dir

    return current_dir

def writeLine(
    out_file, subject_id, video_id, frame_id, fixation_id, person_in_scene):

    """
    Funciton doctring
    """


    with open(out_file, 'a', newline='') as save_file:
        writer = csv.writer(save_file, delimiter='\t')  # tab separated
        if os.stat(out_file).st_size == 0:  # if file is empty, insert header
            writer.writerow((
                'subject_id', 'video_id', 'frame_id',
                'fixation_id', 'person_in_scene'))

        # write trial
        # print(
        #     'WRITE (regular):\n',
        #     [int(str.split(subject_id, '_')[1]), video_id, frame_id,
        #     fixation_id, fixation_dummy[0], fixation_dummy[1],
        #     fixation_dummy[2], fixation_dummy[3]])

        # ? why brackets?
        writer.writerow([
            int(str.split(subject_id, '_')[1]), video_id, frame_id,
            fixation_id, person_in_scene])

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


def readFrames(LOG_FILE):

    """
    Funciton doctring
    """

    with open(LOG_FILE, 'r') as f:

        READER = csv.reader(f, delimiter='\t')
        all_frames = list(READER)
        frames = onlyScreenshotFrames(all_frames)
        # print(frames[:5])

    return frames


def onlyScreenshotFrames(ALL_FRAMES):

    """
    Funciton doctring
    """

    screenshot_frames = []
    for row in ALL_FRAMES[1:]:      # except header
        # video recording starts with frame 230 (250 frames black in the beginning) and video ends at frame 1040, black
        if int(row[3]) % 10 == 0 and 230 <= int(row[3]) <= 1040:

            # print(row)
            screenshot_frames.append(row)

    # print(screenshot_frames)
    return screenshot_frames


# TODO feature saving screenshots?
def saveScreenshotWithFixation(FRAME):
    print("TODO")


# TODO handle keys
def handleInput(NEXT_FRAME):

    """
    Funciton doctring
    """

    print("TODO")

def checkScreenshot(frame_screenshot):

    """
    Funciton doctring
    """

    # check if file is missing
    if not os.path.isfile(frame_screenshot):

        img = np.zeros((840, 756, 3), np.uint8)

        # text
        cv2.putText(
            img,
            'MISSING SCREENSHOT!', (75, 378),
            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))

        missing_screenshot = True

    else:

        missing_screenshot = False
        img = cv2.imread(frame_screenshot)

    return img, missing_screenshot


def getFrameInformation(frame_row, frame_dir):

    """
    Funciton doctring
    """

    video_id = frame_row[2]
    frame_id = frame_row[3]

    gaze_pos_x = int(float(frame_row[4])/2)
    gaze_pos_y = int(float(frame_row[5])/2)

    frame_screenshot = video_id + '_' + 'frame_' + frame_id + '.ppm'
    print('current frame:\t\t', frame_screenshot)
    frame_screenshot = path.join(frame_dir, frame_screenshot)
    frame_screenshot = path.abspath(frame_screenshot)

    return frame_screenshot, video_id, frame_id, gaze_pos_x, gaze_pos_y


def updateImageInformation(image, frame_id, fixation_id, person_in_scene):

    """
    Funciton doctring
    """

    font = cv2.FONT_HERSHEY_PLAIN
    height, width, channels = image.shape

    # frame information box
    cv2.rectangle(
        image,
        (0, height-60), (int(width/1.5), height),
        (0, 0, 0), -1)

    # frame_id
    cv2.putText(
        image,
        'frame_id: ' + frame_id, (0, height-40),
        font, 1, (255, 255, 255))

    # person_in_scene
    cv2.putText(
        image,
        'person_in_scene: ' + person_in_scene, (0, height-25),
        font, 1, (255, 255, 255))

    # fixtiaon_id
    cv2.putText(
        image,
        'current fixation_id: ' + fixation_id, (0, height-12),
        font, 1, (255, 255, 255))

    # update window
    cv2.imshow('frame', image)


def drawFixation(log_file_name, frame_directory='frames'):

    """
    Funciton doctring
    """

    working_dir = here()
    path_files = path.join(working_dir, "02-experiment", "log")
    # extract relevant information from log filename
    subject_id = 'subject_' + str.split(log_file_name, '_')[2]
    part_id = 'session_' + str.split(log_file_name, '_')[4][:-4]
    video_id = log_file_name[18:-4]

    path_files = path.join(path_files, subject_id)
    print("path_files:\t", path_files)

    log_file = path.join(path_files, log_file_name)
    print("log_file:\t", log_file)

    # directory of frames
    frame_dir = path.join(path_files, 'frames', video_id)
    frame_dir = path.abspath(frame_dir)

    # output directory
    out_dir = path.join(
        working_dir, "03-postprocessing",
        "fixations", "log_fixations", subject_id)

    # check if file and folder already exist
    if not path.isdir(out_dir):
        os.makedirs(out_dir)  # throws an error when failing

    out_file = path.join(
        out_dir, str.split(subject_id, '_')[1] + '_' + video_id + '.txt')
    # print(out_file)

    frames = readFrames(log_file)
    # print(frames[:5])
    fixation_id = 'choose from 1 - 4'
    person_in_scene = 'toggle with *p*'

    counter = 0
    while counter < len(frames):

        frame_screenshot, video_id, frame_id, gaze_pos_x, gaze_pos_y = getFrameInformation(frames[counter], frame_dir)

        img, missing = checkScreenshot(frame_screenshot)

        if not missing:

            gaze_position = (gaze_pos_x, gaze_pos_y)  # 216
            cv2.circle(img, gaze_position, 3, (0, 255, 255), 2)
            img = cv2.flip(img, 0)  # 0 = horizontal, 1 = vertical, -1 = both

            updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            cv2.imshow('frame', img)

        else:

            writeLine(
                out_file, subject_id, video_id, frame_id, 'NO_SCREENSHOT',
                'NO_SCREENSHOT')
            counter += 1

        # return(img) https://stackoverflow.com/questions/8381735/how-to-toggle-a-value-in-python
        toggle_person_in_scene = itertools.cycle([
            'persons_in_scene',
            'no_persons_in_scene'])#.__next__

        next_frame = True
        while next_frame and not missing:

            cv2.imshow('frame', img)

            k = cv2.waitKey(33)

            # if missing:
            #     counter += 1
            #     break

            if k == KEY_EXIT:  # Esc

                next_frame = False
                cv2.destroyAllWindows()
                break

            elif k == -1:  # normally -1 returned, so don't print it
                continue

            # toggle person_in_scene
            elif k == KEY_PERSON_IN_SCENE and not missing:

                # TODO needs two toggle, when previous frame was "person_in_scene"
                person_in_scene = next(toggle_person_in_scene)
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            # fixations with person
            elif k == KEY_FIX_PERSON and not missing:  # #1
                fixation_id = 'person'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            elif k == KEY_FIX_OBJECT_MOVING and not missing:  # #2
                fixation_id = 'object_moving'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            elif k == KEY_FIX_OBJECT_STATIC and not missing:  # #3
                fixation_id = 'object_static'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            elif k == KEY_FIX_BACKGROUND and not missing:  # #4
                fixation_id = 'background'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            # special keys
            elif k == KEY_NO_FIXATION and not missing:  # n
                fixation_id = 'no_fixation'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            elif k == KEY_DELETE_FRAME:  # d
                fixation_id = 'delete'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)

            # TODO make a "valid_key = TRUE"
            elif k == KEY_NEXT_FRAME and fixation_id != 'choose from 1 - 4' and person_in_scene != 'toggle with *p*':  # space

                if fixation_id != 'delete':
                    counter += 1
                    writeLine(
                        out_file, subject_id, video_id, frame_id,
                        fixation_id, person_in_scene)

                elif fixation_id == 'delete':
                    counter -= 1
                    fixation_id = 'deleted'
                    deleteLine(out_file)

                break

            else:  # else print key value

                if not missing:
                    fixation_id = 'choose from 1 - 4'
                updateImageInformation(img, frame_id, fixation_id, person_in_scene)
                # print(k)
                # print(repr(chr(k % 256)))  # https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv
                # break

        print('coded fixation_id:\t', fixation_id)
        print('coded person_in_scene:\t', person_in_scene)

        # fixation_id = 'unknown'

        if next_frame is False:
            break


drawFixation(LOG_FILE)
