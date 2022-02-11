import sktechgeek.tracking.hand as hand
import sktechgeek.gesturecontrol.lights.hue as hue
import cv2
import math
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
hand_tracking = hand.HandTracking()
# payload for philips hue
payload = {'bri': 250}
level_bar = 400
level_percentage = 0

while cap.isOpened():
    success, image = cap.read()
    lm_list, image = hand_tracking.get_landmarks(image)

    if len(lm_list) != 0:
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        x3, y3 = lm_list[12][1], lm_list[12][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(image, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

        # color circle
        # cv2.circle(image, (x3, y3), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # color line
        # cv2.line(image, (x1, y1), (x3, y3), (0, 0, 255), 3)
        # cv2.circle(image, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        length = int(math.hypot(x2 - x1, y2 - y1))
        level = int(np.interp(length, [20, 255], [0, 255]))

        lengthHue = int(math.hypot(x3 - x1, y3 - y1))
        levelHue = int(np.interp(lengthHue, [20, 255], [1000, 65000]))

        level_bar = np.interp(length, [20, 255], [400, 150])
        level_percentage = np.interp(length, [20, 255], [0, 100])
        payload = {'bri': level, 'hue': levelHue}

    cv2.rectangle(image, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(image, (50, int(level_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(image, 'Brightness', (5, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 2)
    cv2.putText(image, str(int(level_percentage)) + '%', (100, int(level_bar)), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 2)

    cv2.imshow("Pinch Control", image)
    hue.set_lights('5', payload)

    cv2.waitKey(1)



