import cv2
import mediapipe as mp


class HolisticDetector:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
                                            min_detection_confidence=0.5,
                                            min_tracking_confidence=0.5)

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def find_holistic(self, img):
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
        self.results = self.holistic.process(img_rgb)

        self.mp_draw.draw_landmarks(
            img,
            self.results.face_landmarks,
            self.mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing_styles
                .get_default_face_mesh_tesselation_style())

        self.mp_draw.draw_landmarks(
            img,
            self.results.pose_landmarks,
            self.mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles
                .get_default_pose_landmarks_style())

        self.mp_draw.draw_landmarks(
            img,
            self.results.left_hand_landmarks,
            self.mp_holistic.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())

        self.mp_draw.draw_landmarks(
            img,
            self.results.right_hand_landmarks,
            self.mp_holistic.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())

        return img


def main():
    cap = cv2.VideoCapture(0)
    detector = HolisticDetector()
    while True:
        success, img = cap.read()
        img = detector.find_holistic(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
