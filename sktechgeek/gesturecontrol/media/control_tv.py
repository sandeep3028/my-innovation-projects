import sktechgeek.tracking.hand as hand
import paho.mqtt.publish as publish
import cv2
import sys

hand_tracking = hand.HandTracking()
cap = cv2.VideoCapture(0)
playPressed = False

show = 'yes'

if len(sys.argv) != 2:
    print('Frame show arg is mandatory')
    sys.exit()
show = sys.argv[1]

broker = 'homeassistant'
topic = 'home-assistant/media/options'

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    lm_list, image = hand_tracking.get_landmarks(image)

    gesture = hand_tracking.get_gesture(lm_list)

    if gesture == 'palm':
        cv2.putText(image, "Play", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        publish.single(topic, 'play', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    elif gesture == 'upward_fist':
        cv2.putText(image, "Pause", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        publish.single(topic, 'pause', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    elif gesture == 'straight_fist':
        cv2.putText(image, "Stop", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        publish.single(topic, 'stop', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})

    if show != 'no':
        cv2.imshow("Media Control", image)
    cv2.waitKey(1)
