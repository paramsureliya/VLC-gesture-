import keyboard
import time
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import volumeslider
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################################
wCam, hCam = 640, 480
####################################
x = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.6, trackCon=0.6)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
print(volumeRange)

minVol = volumeRange[0]
maxVol = volumeRange[1]

pTime = 0
cTime = 0
m = 0
while True:
    m = m - 1
    if m < 0:
        m = 0
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

        length = math.hypot(x17 - x8, y17 - y8)
        len1 = y5 - y8
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
        #print(middlefinger_palm_distance)

        if m == 0 and lmlist[8][2] < lmlist[7][2] and lmlist[11][2] > lmlist[12][2] and lmlist[15][2] > lmlist[16][2] and \
                lmlist[19][2] > lmlist[20][2] and lmlist[4][1] > lmlist[3][1] and pause_total_area > 6500 and \
                thumb_lastfinger_distance > 110 and middlefinger_palm_distance > 135:
            m = 30
            keyboard.send("space")
            print(x, pause_total_area, middlefinger_palm_distance)
            x = x + 1
        print(x8)

        if lmlist[8][2] < lmlist[6][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and \
                lmlist[18][2] < lmlist[20][2] and lmlist[4][1] < lmlist[3][1] and area6 > 1.45 and len1 > 45:
            vol = np.interp(x8, [100, 400], [minVol, maxVol])

            print("vol %d" %vol)
            volume.SetMasterVolumeLevel(vol, None)
            cv2.circle(img, (lmlist[8][1], lmlist[8][2]), 15, (255, 0, 255), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
