import cv2
import mediapipe as mp


class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

    def find_faces(self, img):
        """
        When the image file is read with the OpenCV function read() ,
        the order of colors is BGR (blue, green, red). So here we are converting
        BGR image to RGB
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        """
        Processes an RGB image and returns a list of the detected face location data.
        It returns a NamedTuple object with a "detections" field that contains a list of the
        detected face location data.
        """
        self.results = self.face_detection.process(img_rgb)

        if self.results.detections:
            for detection in self.results.detections:
                self.mp_draw.draw_detection(img, detection)

        return img


def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    while True:
        success, img = cap.read()
        img = detector.find_faces(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()


