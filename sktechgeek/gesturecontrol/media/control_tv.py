import sktechgeek.tracking.hand as hand
import paho.mqtt.publish as publish
import cv2
import sys
import time

hand_tracking = hand.HandTracking()
cap = cv2.VideoCapture(0)
playPressed = False

show = 'yes'

if len(sys.argv) != 2:
    print('Frame show arg is mandatory')
    sys.exit()
show = sys.argv[1]

#broker = 'homeassistant'
broker = '192.168.0.199'
topic = 'home-assistant/media/options'
# topic = 'home-assistant/media/opt'

play = False
pause = False
stop = False
power = False
back = False
# volume_up_x_buffer = 200
# volume_down_x_buffer = 400

right_x_buffer = 200
left_x_buffer = 400

sleep_time = 0.3

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    lm_list, image = hand_tracking.get_landmarks(image)
    gesture = hand_tracking.get_gesture(lm_list)
    print(gesture)
    if gesture == 'yo':
        if not power:
            power = True
            publish.single(topic, 'power', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    elif gesture == 'pinky':
        h, w, c = image.shape
        if w - lm_list[20][1] <= right_x_buffer:
            print('Volume Up')
            publish.single(topic, 'volume_up', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
        elif w - lm_list[20][1] >= left_x_buffer:
            print('Volume Down')
            publish.single(topic, 'volume_down', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})

    elif gesture == 'index_middle':
        h, w, c = image.shape
        if w - lm_list[8][1] <= right_x_buffer:
            print('forward')
            publish.single(topic, 'forward', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
        elif w - lm_list[8][1] >= left_x_buffer:
            print('rewind')
            publish.single(topic, 'rewind', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
        time.sleep(sleep_time)
    elif gesture == 'index':
        h, w, c = image.shape
        if w - lm_list[8][1] <= right_x_buffer:
            print('right')
            publish.single(topic, 'right', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
        elif w - lm_list[8][1] >= left_x_buffer:
            print('left')
            publish.single(topic, 'left', hostname=broker,
                           auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
        time.sleep(sleep_time)
    elif gesture == 'palm':
        if not play:
            play = True
            pause = False
            stop = False
            cv2.putText(image, "Play", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            publish.single(topic, 'play', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    elif gesture == 'upward_fist':
        if not pause:
            play = False
            pause = True
            stop = False
            cv2.putText(image, "Pause", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            publish.single(topic, 'pause', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})

    # if gesture == 'index':
    #     publish.single(topic, 'forward', hostname=broker,
    #                        auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    #     time.sleep(sleep_time)
    #
    # elif gesture == 'index_middle':
    #     publish.single(topic, 'rewind', hostname=broker,
    #                        auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    #     time.sleep(sleep_time)
    #
    # elif gesture == 'index_middle_ring':
    #     publish.single(topic, 'volume_up', hostname=broker,
    #                    auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    #     time.sleep(sleep_time)
    #
    # elif gesture == 'index_middle_ring_pinky':
    #     publish.single(topic, 'volume_down', hostname=broker,
    #                    auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    #     time.sleep(sleep_time)
    #
    # elif gesture == 'palm':
    #     if not play:
    #         play = True
    #         pause = False
    #         stop = False
    #         cv2.putText(image, "Play", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    #                     (0, 0, 0), 3)
    #         publish.single(topic, 'play', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})
    #
    # elif gesture == 'upward_fist':
    #     if not pause:
    #         play = False
    #         pause = True
    #         stop = False
    #         cv2.putText(image, "Pause", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    #                     (0, 0, 0), 3)
    #         publish.single(topic, 'pause', hostname=broker, auth={'username': "mqtt-user", 'password': "Mqtt.50786"})



    if show != 'no':
        cv2.imshow("Media Control", image)
    cv2.waitKey(1)
