import sktechgeek.tracking.hand as hand
from pynput.keyboard import Key, Controller
import cv2
import time

hand_tracking = hand.HandTracking()
cap = cv2.VideoCapture(0)
playPressed = False
keyboard = Controller()

play = False
pause = False
stop = False
power = False
back = False

right_x_buffer = 200
left_x_buffer = 400

sleep_time = 0.3

while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    lm_list, image = hand_tracking.get_landmarks(image)
    gesture = hand_tracking.get_gesture(lm_list)
    print(gesture)
    if gesture == 'index_middle':
        h, w, c = image.shape
        if w - lm_list[8][1] <= right_x_buffer:
            print('forward')
            cv2.putText(image, "forward", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.right)
        elif w - lm_list[8][1] >= left_x_buffer:
            print('rewind')
            cv2.putText(image, "rewind", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.left)
        time.sleep(sleep_time)
    elif gesture == 'index':
        h, w, c = image.shape
        if w - lm_list[8][1] <= right_x_buffer:
            print('Volume Up')
            cv2.putText(image, "Volume Up", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.media_volume_up)
        elif w - lm_list[8][1] >= left_x_buffer:
            print('Volume Down')
            cv2.putText(image, "Volume Down", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.media_volume_down)
        time.sleep(sleep_time)
    elif gesture == 'palm':
        if not play:
            play = True
            pause = False
            stop = False
            cv2.putText(image, "Play", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.media_play_pause)
    elif gesture == 'upward_fist':
        if not pause:
            play = False
            pause = True
            stop = False
            cv2.putText(image, "Pause", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 0, 0), 3)
            keyboard.press(Key.media_play_pause)

    cv2.imshow("Media Control", image)
    cv2.waitKey(1)
