import sktechgeek.tracking.pose as pose
import sktechgeek.tracking.hand as hand
import cv2
import os

pose_tracking = pose.PoseTracking()

cap = cv2.VideoCapture(0)
cap.set(3, 1380)  # width
cap.set(4, 820)

text = ''

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)

    lm_list_pose, image = pose_tracking.get_landmarks(image)

    if len(lm_list_pose) != 0:
        if lm_list_pose[14][2] > lm_list_pose[12][2] and lm_list_pose[13][2] > lm_list_pose[11][2] and lm_list_pose[20][2] < lm_list_pose[14][2] and lm_list_pose[19][2] < lm_list_pose[13][2]:
            text = 'Hrithik Coco Cola Step'

    cv2.putText(image, text, (300, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 6)
    cv2.imshow("Dance App", image)
    cv2.waitKey(1)
