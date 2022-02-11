import sktechgeek.tracking.pose as pose
import sktechgeek.tracking.hand as hand
import cv2
import os


hand_tracking = hand.HandTracking()
pose_tracking = pose.PoseTracking()

squatsSelected = False
bicepsCurlSelected = False
shoulderPressSelected = False
pushUpSelected = False

squatsDetected = False
bicepsCurlDetected = False
shoulderPressDetected = False
pushUpDetected = False

squatsCounter = 0
bicepsCurlCounter = 0
shoulderPressCounter = 0
pushUpCounter = 0

headerX = 200
headerY = 200

exercise = 'notselected'
counter = 0


def get_image_list(folder):
    image_list = os.listdir(folder)
    overlay_list = []
    for image_file in image_list:
        image_data = cv2.imread(f'{folder}/{image_file}')
        overlay_list.append(image_data)
    return overlay_list


sidebar_image_list = get_image_list('Sidebar')
counter_image_list = get_image_list('Count')

sidebar = sidebar_image_list[0]
countImage = counter_image_list[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)

    lm_list_hand, image = hand_tracking.get_landmarks(image)
    lm_list_pose, image = pose_tracking.get_landmarks(image)

    if len(lm_list_hand) != 0:
        x, y = lm_list_hand[8][1], lm_list_hand[8][2]
        print(x, y)
        if 0 < y < 125:
            if 600 < x < 750:
                pushUpSelected = True
                squatsSelected = False
                bicepsCurlSelected = False
                shoulderPressSelected = False
                counter, squatsCounter, pushUpCounter, bicepsCurlCounter, shoulderPressCounter = 0, 0, 0, 0, 0
                exercise = 'Push Up'
                sidebar = sidebar_image_list[1]
            elif 800 < x < 950:
                pushUpSelected = False
                squatsSelected = True
                bicepsCurlSelected = False
                shoulderPressSelected = False
                counter, squatsCounter, pushUpCounter, bicepsCurlCounter, shoulderPressCounter = 0, 0, 0, 0, 0
                exercise = 'Squats'
                sidebar = sidebar_image_list[2]
            elif 1000 < x < 1150:
                pushUpSelected = False
                squatsSelected = False
                bicepsCurlSelected = True
                shoulderPressSelected = False
                counter, squatsCounter, pushUpCounter, bicepsCurlCounter, shoulderPressCounter = 0, 0, 0, 0, 0
                exercise = 'Bicep Curl'
                sidebar = sidebar_image_list[3]
            elif 1180 < x < 1280:
                pushUpSelected = False
                squatsSelected = False
                bicepsCurlSelected = False
                shoulderPressSelected = True
                counter, squatsCounter, pushUpCounter, bicepsCurlCounter, shoulderPressCounter = 0, 0, 0, 0, 0
                exercise = 'Shoulder Press'
                sidebar = sidebar_image_list[4]

        cv2.circle(image, (x, y), 10, (255, 0, 0), cv2.FILLED)

    if len(lm_list_pose) != 0:
        if pushUpSelected:
            if lm_list_pose[0][2] > lm_list_pose[14][2] and lm_list_pose[0][2] > lm_list_pose[13][2]:
                if pushUpDetected is False:
                    pushUpDetected = True
                    pushUpCounter = pushUpCounter + 1
                    counter = pushUpCounter

            elif lm_list_pose[0][2] < lm_list_pose[14][2] and lm_list_pose[0][2] < lm_list_pose[13][2]:
                if pushUpDetected:
                    pushUpDetected = False

        elif squatsSelected:
            if lm_list_pose[24][2] > lm_list_pose[26][2] and lm_list_pose[23][2] > lm_list_pose[25][2]:
                if squatsDetected is False:
                    squatsDetected = True
                    squatsCounter = squatsCounter + 1
                    counter = squatsCounter

            elif lm_list_pose[24][2] < lm_list_pose[26][2] and lm_list_pose[23][2] < lm_list_pose[25][2]:
                if squatsDetected:
                    squatsDetected = False

        elif bicepsCurlSelected:
            if lm_list_pose[20][2] < lm_list_pose[14][2]+50 and lm_list_pose[19][2] < lm_list_pose[13][2]+50:
                if bicepsCurlDetected is False:
                    bicepsCurlDetected = True
                    bicepsCurlCounter = bicepsCurlCounter + 1
                    counter = bicepsCurlCounter

            elif lm_list_pose[20][2] > lm_list_pose[14][2] and lm_list_pose[19][2] > lm_list_pose[13][2]:
                if bicepsCurlDetected:
                    bicepsCurlDetected = False

        elif shoulderPressSelected:
            if lm_list_pose[14][2] > lm_list_pose[12][2] and lm_list_pose[13][2] > lm_list_pose[11][2] and lm_list_pose[20][2] < lm_list_pose[14][2] and lm_list_pose[19][2] < lm_list_pose[13][2]:
                if shoulderPressDetected is False:
                    shoulderPressDetected = True
                    shoulderPressCounter = shoulderPressCounter + 1
                    counter = shoulderPressCounter

            elif lm_list_pose[14][2] < lm_list_pose[12][2] and lm_list_pose[13][2] < lm_list_pose[11][2] and lm_list_pose[20][2] < lm_list_pose[14][2] and lm_list_pose[19][2] < lm_list_pose[13][2]:
                if shoulderPressDetected:
                    shoulderPressDetected = False

    if exercise != 'notselected':
        cv2.putText(image, exercise+" : " + str(counter), (headerX, headerY), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),
                5)
        if counter < 6:
            countImage = counter_image_list[counter]
            image[125:225, 0: 100] = countImage
    image[0:125, 0:1280] = sidebar

    cv2.imshow("Excercise App", image)

    cv2.waitKey(1)

