import sktechgeek.tracking.hand as hand
import cv2
import requests

url_forward = "http://192.168.0.159:5000/motor/forward"
url_backward = "http://192.168.0.159:5000/motor/backward"
url_right = "http://192.168.0.159:5000/motor/right"
url_left = "http://192.168.0.159:5000/motor/left"
url_stop = "http://192.168.0.159:5000/motor/stop"
led_on = "http://192.168.0.159:5000/led/on"

forward = False
stop = False
right_x_buffer = 200
left_x_buffer = 400

hand_tracking = hand.HandTracking()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    lm_list, image = hand_tracking.get_landmarks(image)
    gesture = hand_tracking.get_gesture(lm_list)

    if gesture == 'palm':
        requests.get(url_forward)
        print('forward')
    elif gesture == 'upward_fist':
        requests.get(url_stop)
        print('stop')
    elif gesture == 'thumbs_up':
        requests.get(url_backward)
        print("backward")
    elif gesture == 'index':
        h, w, c = image.shape
        if w - lm_list[8][1] <= right_x_buffer:
            requests.get(url_right)
            print('right')
        elif w - lm_list[8][1] >= left_x_buffer:
            requests.get(url_left)
            print('left')
    elif gesture == 'pinky':
        requests.get(led_on)

    cv2.imshow("Media Control", image)
    cv2.waitKey(1)
