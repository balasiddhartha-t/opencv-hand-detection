import cv2
import time
import numpy as np
import HandTrackingModule  as htm
wCam, hCam = 640, 480
import math


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


from subprocess import call
call(["amixer", "-D", "pulse", "sset", "Master", "0%"])


detector = htm.handDetector(detectionCon=0.6)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw= False)
    # print(lmlist)

    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range 20 - 300
        # Volume Range 0 - 100
        vol = np.interp(length, [30, 150], [0, 100])
        print(vol)
        if length < 20:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        call(["amixer", "-D", "pulse", "sset", "Master", str(vol)+"%"])

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
    cv2.imshow("Img", img)
    cv2.waitKey(1)
