import mediapipe as mp
import cv2


class HandTracking():

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def get_landmarks(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        lm_list = []
        if results.multi_hand_landmarks:
            my_hand = results.multi_hand_landmarks[0]
            for lmId, lm in enumerate(my_hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([lmId, cx, cy])
            if draw:
                self.mpDraw.draw_landmarks(image, my_hand, self.mpHands.HAND_CONNECTIONS)
        return lm_list, image

    @staticmethod
    def get_gesture(lm_list):
        gesture = ''
        if len(lm_list) != 0:
            if lm_list[20][2] < lm_list[20 - 2][2] and lm_list[16][2] < lm_list[16 - 2][2] and lm_list[12][2] < \
                    lm_list[12 - 2][
                        2] and lm_list[8][2] < lm_list[8 - 2][2] and lm_list[4][1] < lm_list[4 - 1][1]:
                gesture = 'palm'
            elif lm_list[20][2] > lm_list[20 - 2][2] and lm_list[16][2] > lm_list[16 - 2][2] and lm_list[12][2] > \
                    lm_list[12 - 2][
                        2] and lm_list[8][2] > lm_list[8 - 2][2] and lm_list[4][1] > lm_list[4 - 1][1]:
                gesture = 'upward_fist'
            elif lm_list[8][2] > lm_list[0][2]:
                gesture = 'straight_fist'
        return gesture


def main():
    cap = cv2.VideoCapture(0)
    hand_tracking = HandTracking()

    while cap.isOpened():
        success, image = cap.read()
        lm_list, image = hand_tracking.get_landmarks(image)

        cv2.imshow("Frame", image)
        print(lm_list)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()











