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
import pandas as pd

# set to true, if you want to see the accuracy, 500ms per frame
VISUALIZE_DRIFT = True

# set to true, if you want to safe the results to "log_validation/"
EXPORT_RESULTS = False

def calculate_drift(data_dir):

    """
    TODO: calculate_drift(data_dir)-docstring
    """

    validation_log = []

    # for each subject in directory
    for i in os.listdir(data_dir):
        subject_id = i
        file_path = path.join(data_dir, subject_id)
        file_path = path.abspath(file_path)

        files_id = '_'.join(str.split(os.listdir(file_path)[1], '_')[:-2])
        # print(files_id)

        # output directory
        out_dir = path.join('log_validation', subject_id)
        out_dir = path.abspath(out_dir)

        if EXPORT_RESULTS:
            # check if file and folder already exist
            if not path.isdir(out_dir):
                os.makedirs(out_dir)  # throws an error when failing

        # for each validation video
        for part in [1, 2]:

            val_before_id = 'val_1_' + str(part)
            val_after_id = 'val_2_' + str(part)

            val_before_file_name = '_'.join((files_id, val_before_id)) + ".txt"
            val_after_file_name = '_'.join((files_id, val_after_id)) + ".txt"

            # use dictionary like: val_files {path:, file: , name: }
            val_files = [
                path.join(file_path, val_before_file_name),
                path.join(file_path, val_after_file_name)]

            val_files[0] = path.abspath(val_files[0])
            val_files[1] = path.abspath(val_files[1])

            correct_drift(val_files, out_dir, validation_log)

    return validation_log


def filter_frames(all_frames):

    """
    TODO: filter_frames-docstring
    """

    screenshot_frames = []
    for row in all_frames[1:]:      # except header

        # only every 10th screenshot taken
        every_10th = (int(row[3]) % 10 == 0 and int(row[3]) >= 230)

        # frames when validation points are highlighted for fixation
        only_white = (
            (250 <= int(row[3]) <= 490) or    # green 1
            (550 <= int(row[3]) <= 790) or    # blue 1
            (850 <= int(row[3]) <= 1090) or   # red 1
            (1250 <= int(row[3]) <= 1490) or  # green 2
            (1550 <= int(row[3]) <= 1790) or  # blue 2
            (1850 <= int(row[3]) <= 2090))    # red 2

        if every_10th and only_white:

            # print(row)
            screenshot_frames.append(row)

    # print(screenshot_frames)
    return screenshot_frames


def read_frames(log_file):

    """
    TODO: read_frames-docstring
    """

    with open(log_file, 'r') as file:

        reader = csv.reader(file, delimiter='\t')
        all_frames = list(reader)

        subject_id = all_frames[1][0]
        video_id = all_frames[1][2]

        video_part = video_id[-1]
        video_id = video_id[0:-2]

        frames = filter_frames(all_frames)
        # print(frames[:5])

    return subject_id, video_id, video_part, frames


def prepare_image(control_x, control_y, gaze_x, gaze_y, res, contours, img):

    """
    TODO: read_frames-docstring
    """

    diff_x = (control_x - gaze_x)
    diff_y = (control_y - gaze_y)

    # res not shown atm
    cv2.drawContours(
        image=res, contours=contours, contourIdx=-1,
        color=(0, 255, 255), thickness=-1)

    cv2.circle(
        img=res, center=(control_x, control_y), radius=2,
        color=(255, 255, 0), thickness=-1)

    # show fixation (turquoise) and roi (white)
    cv2.circle(
        img=img, center=(control_x, control_y),
        radius=10, color=(255, 255, 255), thickness=2)

    cv2.circle(
        img=img, center=(gaze_x, gaze_y),
        radius=10, color=(255, 255, 0), thickness=2)

    cv2.circle(
        img=img, center=(gaze_x, gaze_y),
        radius=2, color=(255, 255, 0), thickness=-1)

    text = 'Difference x: ' + str(diff_x) + "; Difference y: " + str(diff_y)
    cv2.putText(
        img=img, text=text,
        org=(75, 378),
        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
        color=(255, 255, 255))

    return img, res


def show_image(res, img):

    """
    TODO: read_frames-docstring
    """

    # show
    cv2.imshow('frame', img)

    # cv2.imshow('thresh', thresh)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)

    cv2.waitKey(100)


def correct_drift(validation_files, out_dir, validation_log):

    """
    TODO: correct_drift-docstring
    Find Val_X_1 and VA_X_2 and compute drift correction
    """

    for file in range(len(validation_files)):

        frames = []
        frame_log = []
        subject_id, video_id, video_part, frames = read_frames(validation_files[file])

        if video_id[-1] == "1":
            validation_id = "pre"
        else:
            validation_id = "post"
        #print(validation_files[file][0])
        #print(video_part)

        # print(validation_id)
        # print(frames[:5])


        frame_dir = path.join('log', "subject_" + subject_id, 'frames', video_id + "_" + video_part)
        out_file = path.join(
            out_dir,
            subject_id + "_" + video_id + "_" + video_part + '.txt')
        # print(out_file)

        if not frames:

            print("missing\t\t", subject_id, "\t",
                video_id, "\t", video_part, "\t", validation_id)
            if EXPORT_RESULTS:
                with open(out_file, 'w', newline='') as save_file:

                    writer = csv.writer(save_file, delimiter='\t')  # tab

                    if os.stat(out_file).st_size == 0:  # if empty, insert header
                        writer.writerow(
                            ['subject_id', 'video_id', 'video_part',
                            'validation_id', 'validation_time', 'validation_point',
                            'frame_id', 'gaze_x', 'gaze_y', 'control_x',
                            'control_y'])

                    writer.writerow(
                        [subject_id, video_id, video_part,
                        validation_id, '', '',
                        '', '', '', '', ''])

        else:

            print("working on\t", subject_id, "\t",
                video_id, "\t", video_part, "\t", validation_id)

            for i in range(len(frames)):
                frame = frames[i]

                frame_id = frame[3]
                # print("THIS IS VALIDATION FRAME ID:", frame_id)

                # log which point should be fixated
                if 250 <= int(frame_id) <= 490:
                    validation_point = 'green'
                    validation_time = '1'
                elif 550 <= int(frame_id) <= 790:
                    validation_point = 'blue'
                    validation_time = '1'
                elif 850 <= int(frame_id) <= 1090:
                    validation_point = 'red'
                    validation_time = '1'
                elif 1250 <= int(frame_id) <= 1490:
                    validation_point = 'green'
                    validation_time = '2'
                elif 1550 <= int(frame_id) <= 1790:
                    validation_point = 'blue'
                    validation_time = '2'
                elif 1850 <= int(frame_id) <= 2090:
                    validation_point = 'red'
                    validation_time = '2'

                frame_screenshot = video_id + '_' + video_part + "_" + 'frame_' + frame_id + '.ppm'
                # print('current validation frame:\t\t', frame_screenshot)
                frame_screenshot = path.join(frame_dir, frame_screenshot)
                # print(frame_screenshot)

                frame_screenshot = path.abspath(frame_screenshot)
                # print('current validation frame:\t\t', frame_screenshot)

                img = cv2.imread(frame_screenshot)

                gaze_position = (int(float(frame[4])/2),
                                 int(float(frame[5])/2))

                gaze_x = gaze_position[0]
                gaze_y = gaze_position[1]

                # https://stackoverflow.com/questions/22588146/tracking-white-color-using-python-opencv
                hsv = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2HSV)
                sensitivity = 125
                lower_white = np.array([0, 0, 255-sensitivity])
                upper_white = np.array([255, sensitivity, 255])

                # Threshold the HSV image to get only white colors
                mask = cv2.inRange(
                    src=hsv, lowerb=lower_white, upperb=upper_white)
                # Bitwise-AND mask and original image
                res = cv2.bitwise_and(
                    src1=img, src2=img, mask=mask)

                # finding contours
                # ret, thresh = cv2.threshold(mask, 127, 255, 0)

                # check opencv-python version to also run on older versions
                if int(cv2.__version__[0]) >= 4:
                    contours, hierarchy = cv2.findContours(
                        image=mask,
                        mode=cv2.RETR_TREE,
                        method=cv2.CHAIN_APPROX_SIMPLE)

                # relevant e.g. for psychopy opencv
                else:
                    image, contours, hierarchy = cv2.findContours(
                        image=mask,
                        mode=cv2.RETR_TREE,
                        method=cv2.CHAIN_APPROX_SIMPLE)

                """
                assume perfect fixation:
                only filtered frames so each frame has a white spot if it is
                not covert by fixation and missing contours
                """
                if not contours:
                    # print("no contours: ", frame_id, "\t1")
                    frame_log.append(
                        [subject_id, video_id, video_part,
                         validation_id, validation_time, validation_point,
                         frame_id, gaze_x, gaze_y, '', ''])
                    validation_log.append(
                        [subject_id, video_id, video_part,
                         validation_id, validation_time, validation_point,
                         frame_id, gaze_x, gaze_y, '', ''])

                else:

                    # sorting contours by size
                    contours = sorted(
                        contours,
                        key=cv2.contourArea,
                        reverse=True)

                    # for c in contours:
                    # compute the center of the contour
                    contour_moment = cv2.moments(array=contours[0])

                    if contour_moment['m00'] > 0:

                        # print("M > 0\t\t\t\t", frame_id)
                        control_x = int(
                            contour_moment["m10"] / contour_moment["m00"])
                        control_y = int(
                            contour_moment["m01"] / contour_moment["m00"])

                        frame_log.append(
                            [subject_id, video_id, video_part,
                             validation_id, validation_time, validation_point,
                             frame_id, gaze_x, gaze_y, control_x, control_y])
                        validation_log.append(
                            [subject_id, video_id, video_part,
                             validation_id, validation_time, validation_point,
                             frame_id, gaze_x, gaze_y, control_x, control_y])

                        if VISUALIZE_DRIFT:
                            prepare_image(control_x, control_y, gaze_x, gaze_y,
                                          res, contours, img)

                    else:
                        # print("no contours: ", frame_id, "\t2")
                        frame_log.append(
                            [subject_id, video_id, video_part,
                             validation_id, validation_time, validation_point,
                             frame_id, gaze_x, gaze_y, '', ''])
                        validation_log.append(
                            [subject_id, video_id, video_part,
                             validation_id, validation_time, validation_point,
                             frame_id, gaze_x, gaze_y, control_x, control_y])

                    if VISUALIZE_DRIFT:
                        show_image(res, img)

            if EXPORT_RESULTS:
                with open(out_file, 'w', newline='') as save_file:
                    writer = csv.writer(save_file, delimiter='\t')
                    if os.stat(out_file).st_size == 0:
                        writer.writerow([
                            'subject_id', 'video_id', 'video_part',
                            'validation_id', 'validation_time', 'validation_point',
                            'frame_id', 'gaze_x', 'gaze_y', 'control_x',
                            'control_y'])

                    writer.writerows(frame_log)

validation_log = calculate_drift("log")
header = ['subject_id', 'video_id', 'video_part',
                         'validation_id', 'validation_time', 'validation_point',
                         'frame_id', 'gaze_x', 'gaze_y', 'control_x',
                         'control_y']

# for reticulate if done with in rstudio
validation_log = pd.DataFrame(validation_log, columns=header)
print("done")

if VISUALIZE_DRIFT:
    cv2.destroyAllWindows()