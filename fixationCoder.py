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
import glob
import csv
import cv2
import numpy as np
import itertools

#############################################################################
################# Settings  #################################################
#############################################################################

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

def here(file_name='.here'):

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
            # print('File Exists in: ', current_dir)
            break

        else:
            if current_dir == parent_dir:  # if dir is root dir
                # print('File not found')
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


# TODO handle keys
def handleInput(NEXT_FRAME):

    """
    Funciton doctring
    """

    print('TODO')


# TODO
def checkInputKey(key1, key2):

    """
    Funciton doctring
    """

    if not key2 != 'choose from 1 - 4' or key2 != 'deleted' and key1 != 'toggle with *p*':
        valid_key = True
    else:
        valid_key = False

    return valid_key


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


# TODO
def togglePersonInScene():

    """
    Function docstring
    """


# TODO
def prepareFrames():

    """
    Prepares images for rating: Picks information and according frame and draws gaze point into frame for rating.
    Returns img ready for rating (similiar to RL frames).
    """


def runFixationCoder(path_to_frames):

    all_frames = []
    all_frames.extend(
        glob.glob(os.path.join(path_to_frames, "*.png")))

    #print(all_frames)
    print(all_frames[:5])
    fixation_id = 'choose from 1 - 4'
    person_in_scene = 'toggle with *p*'

    # initialize toggle
    toggle_person_in_scene = True
    missing = False

    counter = 0
    while counter < len(all_frames):

        frame_id = all_frames[counter][-8:-4]
        frame_img = cv2.imread(all_frames[counter])
        print(frame_id)
        updateImageInformation(frame_img, frame_id, fixation_id, person_in_scene)
        cv2.imshow('frame', frame_img)


        next_frame = True
        while next_frame and not missing:

            cv2.imshow('frame', frame_img)

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

                toggle_person_in_scene = not toggle_person_in_scene

                if not toggle_person_in_scene:
                    person_in_scene = 'no_person_in_scene'
                else:
                    person_in_scene = 'person_in_scene'

                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            # fixations with person
            elif k == KEY_FIX_PERSON and not missing:  # #1
                fixation_id = 'person'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            elif k == KEY_FIX_OBJECT_MOVING and not missing:  # #2
                fixation_id = 'object_moving'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            elif k == KEY_FIX_OBJECT_STATIC and not missing:  # #3
                fixation_id = 'object_static'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            elif k == KEY_FIX_BACKGROUND and not missing:  # #4
                fixation_id = 'background'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            # special keys
            elif k == KEY_NO_FIXATION and not missing:  # n
                fixation_id = 'no_fixation'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            elif k == KEY_DELETE_FRAME:  # d
                fixation_id = 'delete'
                updateImageInformation(frame_img, frame_id, fixation_id,
                                       person_in_scene)

            # ! WIP make a "valid_key = TRUE"
            elif k == KEY_NEXT_FRAME and checkInputKey(person_in_scene, fixation_id):  # space

                if fixation_id != 'delete':
                    counter += 1
                    # writeLine(
                    #     out_file, subject_id, video_id, frame_id,
                    #     fixation_id, person_in_scene)

                elif fixation_id == 'delete':
                    counter -= 1
                    fixation_id = 'deleted'
                    # deleteLine(out_file)

                break

            else:  # else print key value

                if not missing:
                    fixation_id = 'choose from 1 - 4'
                updateImageInformation(img, frame_id, fixation_id,
                                       person_in_scene)
                # print(k)
                # print(repr(chr(k % 256)))  # https://stackoverflow.com/questions/14494101/using-other-keys-for-the-waitkey-function-of-opencv
                # break

        print('coded fixation_id:\t', fixation_id)
        print('coded person_in_scene:\t', person_in_scene)

        # fixation_id = 'unknown'

        if next_frame is False:
            break

def presentImage(img):
    
    """
    Presents given img to rater for rating
    """

# log file
LOG_FILE = path.join(here(), '03-preprocessing', 'frames_with_gaze', '99', 'txt', '2.8', '2')


runFixationCoder(LOG_FILE)
# runFixationCoder()

