# Computer vision - car counter
# Written by Alex Timokhov and Ilya Golan for Tel-Hai Collage
#*****************************************************************************************************
#***************Both of the folders below have to be created before working with program**************
#*****************************************************************************************************
# Input video default location - C:/videos
# output frames default location - C:/output
import os
import re
import cv2
import numpy as np
from os.path import isfile, join
import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.


print('Please choose the direction number of capture: ')
print("1 - north")
print("2 - south")
print("3 - east")
print("4 - west")
directionstr = input()
direction = int(directionstr)
print('running...')
if direction >4 or direction < 1:
    print('wrong selection!')
    quit()

# Tweak video name and or location to run
capture = cv2.VideoCapture('C:/videos/video.mp4')

frameNr = 0

while (True):

    success, frame = capture.read()

    if success:
        cv2.imwrite(f'C:/output/frame_{frameNr}.jpg', frame)

    else:
        break

    frameNr = frameNr + 1

capture.release()


# get file names of the frames
# frameList = os.listdir('frames/')
frameList = os.listdir('C:/output/')

# sort file names
frameList.sort(key=lambda f: int(re.sub('\D', '', f)))

# empty list to store the frames
originalFrames = []

frameHeight = 0
frameWidth = 0
for frameName in frameList:
    # read the frames
    # img = cv2.imread('frames/' + frameName)
    img = cv2.imread('C:/output/' + frameName)
    # append the frames to the list
    originalFrames.append(img)
    frameHeight, frameWidth, layers = img.shape

# print("types 1 are ", frameHeight, " ", frameWidth)



# plot 13th frame
# i = 13
#
# for frame in [i, i+1]:
#     plt.imshow(cv2.cvtColor(originalFrames[frame], cv2.COLOR_BGR2RGB))
#     plt.title("frame: " + str(frame))
#     plt.show()


# kernel for image dilation
kernel = np.ones((4, 4), np.uint8)

# font style
font = cv2.FONT_HERSHEY_SIMPLEX

# directory to save the ouput frames
editedFramesFolder = "editedFrames/"
numCarsInLastFrame = 0
numTotalCars = 0

numName = 0
# for i in range(len(originalFrames) - 1):
for i in range(0, len(originalFrames) - 1, 2):

    # frame differencing
    grayFrame1 = cv2.cvtColor(originalFrames[i], cv2.COLOR_BGR2GRAY)
    grayFrame2 = cv2.cvtColor(originalFrames[i + 1], cv2.COLOR_BGR2GRAY)
    frameDifferance = cv2.absdiff(grayFrame2, grayFrame1)

    # image thresholding
    ret, threshold = cv2.threshold(frameDifferance, 30, 255, cv2.THRESH_BINARY)

    # image dilation
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    # find contours
    contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    editedFrame = originalFrames[i].copy()

    height, width, layers = editedFrame.shape


    # shortlist contours appearing in the detection zone
    contoursInZone = []
    for cntr in contours:
        x, y, w, h = cv2.boundingRect(cntr)
        # if (x <= 1100) & (y >= 350) & (cv2.contourArea(cntr) >= 3550):
        # if (x >= 800) & (y >= 0) & (cv2.contourArea(cntr) >= 4750):

        # Dependig on video resolution and zoom cv2.contourArea may need changin for proper detection in all cases
        if direction == 1:
            if (x >= 0) & (y <= frameHeight//3) & (cv2.contourArea(cntr) >= 4750):
                contoursInZone.append(cntr)
                # get the xmin, ymin, width, and height coordinates from the contours
                (x, y, w, h) = cv2.boundingRect(cntr)
                # draw the bounding boxes
                cv2.rectangle(editedFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        elif direction == 2:
            if (x >= 0) & (y >= frameHeight*2//3) & (cv2.contourArea(cntr) >= 4750):
                contoursInZone.append(cntr)
                # get the xmin, ymin, width, and height coordinates from the contours
                (x, y, w, h) = cv2.boundingRect(cntr)
                # draw the bounding boxes
                cv2.rectangle(editedFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        elif direction == 3:
            if (x >= frameWidth*2//3) & (y >= 0) & (cv2.contourArea(cntr) >= 4750):
                contoursInZone.append(cntr)
                # get the xmin, ymin, width, and height coordinates from the contours
                (x, y, w, h) = cv2.boundingRect(cntr)
                # draw the bounding boxes
                cv2.rectangle(editedFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        elif direction == 4:
            if (x <= frameWidth//3) & (y >= 0) & (cv2.contourArea(cntr) >= 4750):
                contoursInZone.append(cntr)
                # get the xmin, ymin, width, and height coordinates from the contours
                (x, y, w, h) = cv2.boundingRect(cntr)
                # draw the bounding boxes
                cv2.rectangle(editedFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if len(contoursInZone) > numCarsInLastFrame:
        numTotalCars += len(contoursInZone) - numCarsInLastFrame
    numCarsInLastFrame = len(contoursInZone)

    cv2.putText(editedFrame, "cars counted: " + str(numTotalCars), (frameWidth//4, frameHeight//4), font, 3, (0, 0, 255), 5)
    # cv2.line(editedFrame, (0, 350), (1275, 350), (0, 0, 255), 2)
    if direction == 1:
        cv2.line(editedFrame, (0, frameHeight//3), (frameWidth, frameHeight//3), (0, 0, 255), 2)
    elif direction == 2:
        cv2.line(editedFrame, (0, frameHeight*2//3), (frameWidth, frameHeight*2//3), (0, 0, 255), 2)
    elif direction == 3:
        cv2.line(editedFrame, (frameWidth*2//3, 0), (frameWidth*2//3, frameHeight), (0, 0, 255), 2)
    elif direction == 4:
        cv2.line(editedFrame, (frameWidth//3, 0), (frameWidth//3, frameHeight), (0, 0, 255), 2)
    cv2.imwrite(editedFramesFolder + str(numName) + '.png', editedFrame)
    numName += 1

# specify video name
newVideoName = 'productVideo.avi'

# specify frames per second
fps = 14.0

editedFrameArray = []
files = [f for f in os.listdir(editedFramesFolder) if isfile(join(editedFramesFolder, f))]

files.sort(key=lambda f: int(re.sub('\D', '', f)))

for i in range(len(files)):
    filename = editedFramesFolder + files[i]

    # read frames
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)

    # inserting the frames into an image array
    editedFrameArray.append(img)
    # print("types 2 are ", height, " ", width)

newVideo = cv2.VideoWriter(newVideoName, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(editedFrameArray)):
    # writing to a image array
    newVideo.write(editedFrameArray[i])

newVideo.release()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Done, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('and Done.')

