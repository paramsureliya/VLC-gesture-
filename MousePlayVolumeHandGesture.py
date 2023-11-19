import keyboard
from pynput.mouse import Button, Controller
import wx
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


mouse = Controller()
app = wx.App(False)


####################################
wCam, hCam = 640, 480
####################################
mouse_counter = 0
leftclick_counter = 0
pause_counter = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.6, trackCon=0.6)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()

minVol = volumeRange[0]
maxVol = volumeRange[1]

pTime = 0
cTime = 0
while True:
    leftclick_counter = leftclick_counter - 1
    if leftclick_counter < 0:
        leftclick_counter = 0
    mouse_counter = mouse_counter - 1
    if mouse_counter < 0:
        mouse_counter = 0
    pause_counter = pause_counter - 1
    if pause_counter < 0:
        pause_counter = 0
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8])

        x8, y8 = lmlist[8][1], lmlist[8][2]
        x17, y17 = lmlist[17][1], lmlist[17][2]
        x0, y0 = lmlist[0][1], lmlist[0][2]
        x2, y2 = lmlist[2][1], lmlist[2][2]
        x10, y10 = lmlist[10][1], lmlist[10][2]
        x5, y5 = lmlist[5][1], lmlist[5][2]
        x4, y4 = lmlist[4][1], lmlist[4][2]
        x12, y12 = lmlist[12][1], lmlist[12][2]
        x20, y20 = lmlist[20][1], lmlist[20][2]

        cv2.circle(img, (x8, y8), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x17, y17), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x0, y0), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x10, y10), 10, (255, 255, 0), cv2.FILLED)
        cv2.line(img, (x10, y10), (x2, y2), (255, 255, 0), 3)
        cv2.line(img, (x17, y17), (x10, y10), (255, 255, 0), 3)
        cv2.line(img, (x17, y17), (x8, y8), (255, 0, 0), 3)
        cv2.line(img, (x17, y17), (x0, y0), (255, 0, 0), 3)
        cv2.line(img, (x0, y0), (x2, y2), (255, 0, 0), 3)
        cv2.line(img, (x8, y8), (x2, y2), (255, 0, 0), 3)
        cv2.line(img, (x0, y0), (x20, y20), (255, 0, 255), 3)
        cv2.line(img, (x20, y20), (x12, y12), (255, 0, 255), 3)
        cv2.line(img, (x4, y4), (x0, y0), (255, 0, 255), 3)
        cv2.line(img, (x4, y4), (x12, y12), (255, 0, 255), 3)
        cv2.line(img, (x4, y4), (x8, y8), (0, 0, 255), 3)
        # print('value of tip of finger is %d ' % x8)

        matrix_area1 = [[x0, y0, 1], [x17, y17, 1], [x2, y2, 1]]
        area1 = abs(0.5 * np.linalg.det(matrix_area1))
        matrix_area2 = [[x17, y17, 1], [x2, y2, 1], [x8, y8, 1]]
        area2 = abs(0.5 * np.linalg.det(matrix_area2))
        area3 = area1 + area2
        matrix_area4 = [[x17, y17, 1], [x2, y2, 1], [x10, y10, 1]]
        area4 = abs(0.5 * np.linalg.det(matrix_area4))
        area5 = area1 + area4
        area6 = area3 / area5

        #length = math.hypot(x17 - x8, y17 - y8)
        length = math.hypot(x4 - x8, y4 - y8)
        (cx, cy) = ((x8+x4+x17)//3), ((y4+y8+y17)//3)
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        len1 = y5 - y8
        print(length)
        # print(len1)
        # print("length is %d,area1 is %d, %d area2 is, len1 is %d, ratio = %0.2f" % (length, area3, area5, len1, area6))
        # # print(length)

        # hand range 50- 200
        # vol range -65.25 - 0

        pause_area1_matrix = [[x0, y0, 1], [x4, y4, 1], [x12, y12, 1]]
        pause_area1 = abs(0.5 * np.linalg.det(pause_area1_matrix))
        pause_area2_matrix = [[x0, y0, 1], [x20, y20, 1], [x12, y12, 1]]
        pause_area2 = abs(0.5 * np.linalg.det(pause_area2_matrix))
        pause_total_area = pause_area1 + pause_area2
        thumb_lastfinger_distance = x4 - x20
        middlefinger_palm_distance = y0 - y12

        mouse_matrix_area1 = [[x4, y4, 1], [x8, y8, 1], [x2, y2, 1]]
        mouse_area1 = abs(0.5 * np.linalg.det(mouse_matrix_area1))
        total_mouse_area = area3 + mouse_area1
        area7 = total_mouse_area / area3
        area8 = total_mouse_area / area5
        print(area7, area8, area6, len1)


        thumb_palm_distance = y4 - y5
        fstfinger_middlefinger_distance = y8 - y12
        # print(pause_total_area, thumb_palm_distance, fstfinger_middlefinger_distance)

        if lmlist[8][2] < lmlist[6][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and \
                lmlist[18][2] < lmlist[20][2] and lmlist[3][1] < lmlist[4][1] and area6 > 1.45 and len1 > 45 and area8 > 2.2:
            mouse_x = np.interp(cx, [210, 550], [0, 1380])      #  mouse_x = np.interp(cx, [180, 590], [0, 1366])
            mouse_y = np.interp(cy, [130, 370], [0, 768])        # mouse_y = np.interp(cy, [100, 400], [0, 768])
            mouse.position = (mouse_x, mouse_y)
            mouse_counter = 10

        if lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and \
                lmlist[18][2] < lmlist[20][2] and length < 20 and 10 > mouse_counter > 0 and leftclick_counter == 0 :
            print("left click")
            mouse.press(Button.left)
            mouse.release(Button.left)
            leftclick_counter = 3

        if pause_counter == 0 and lmlist[8][2] < lmlist[7][2] and lmlist[11][2] > lmlist[12][2] and lmlist[15][2] > lmlist[16][2] and \
                lmlist[19][2] > lmlist[20][2] and lmlist[4][1] > lmlist[3][1] and pause_total_area > 6500 and \
                thumb_lastfinger_distance > 110 and middlefinger_palm_distance > 135 and leftclick_counter == 0:
            pause_counter = 30
            keyboard.send("space")
            print(pause_total_area, middlefinger_palm_distance)


        if lmlist[8][2] < lmlist[6][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and \
                lmlist[18][2] < lmlist[20][2] and lmlist[4][1] < lmlist[3][1] and area6 > 1.45 and len1 > 45 and mouse_counter < 1:
            vol = np.interp(x8, [50, 550], [minVol, maxVol])
            print("vol %d" %vol)
            volume.SetMasterVolumeLevel(vol, None)
            cv2.circle(img, (lmlist[8][1], lmlist[8][2]), 15, (255, 0, 255), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
