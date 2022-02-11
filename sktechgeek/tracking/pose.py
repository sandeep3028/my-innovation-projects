import mediapipe as mp
import cv2


class PoseTracking():

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(model_complexity=2,
                                      enable_segmentation=True)

    def get_landmarks(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        lm_list = []
        if results.pose_landmarks:
            my_pose = results.pose_landmarks
            for lmId, lm in enumerate(my_pose.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([lmId, cx, cy])

            if draw:
                self.mp_drawing_utils.draw_landmarks(image,
                                                     my_pose,
                                                     self.mp_pose.POSE_CONNECTIONS,
                                                     landmark_drawing_spec=self.mp_drawing_styles.
                                                     get_default_pose_landmarks_style())
        return lm_list, image


def main():
    cap = cv2.VideoCapture(0)
    pose = PoseTracking()

    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        lm_list, image = pose.get_landmarks(image)

        cv2.imshow("Frame", image)
        print(lm_list)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
