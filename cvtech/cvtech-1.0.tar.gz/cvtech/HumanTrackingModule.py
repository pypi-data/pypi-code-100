import cv2
import mediapipe as mp


class HumanDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def find_humans(self, img):
        """
        When the image file is read with the OpenCV function read() ,
        the order of colors is BGR (blue, green, red). So here we are converting
        BGR image to RGB
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        """
        Processes an RGB image and returns the hand landmarks and handedness of each detected hand.
        It returns a NamedTuple object with two fields: a "multi_hand_landmarks" field that
        contains the hand landmarks on each detected hand and a "multi_handedness"
        field that contains the handedness (left v.s. right hand) of the detected
        hand.
        """
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                img,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

        return img


def main():
    cap = cv2.VideoCapture(0)
    detector = HumanDetector()
    while True:
        success, img = cap.read()
        img = detector.find_humans(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
