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











