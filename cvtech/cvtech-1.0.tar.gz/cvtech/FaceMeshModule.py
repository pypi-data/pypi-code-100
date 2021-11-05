import cv2
import mediapipe as mp


class FaceMeshDetector:
    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh

        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=0.5, circle_radius=1)
        self.faceMesh = self.mp_face_mesh.FaceMesh(max_num_faces=1,
                                                   refine_landmarks=True,
                                                   min_detection_confidence=0.5,
                                                   min_tracking_confidence=0.5)

    def find_faceMesh(self, img):
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
        self.results = self.faceMesh.process(img_rgb)

        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                self.mp_draw.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style())

                self.mp_draw.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())

                self.mp_draw.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_iris_connections_style())

        return img


def main():
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        img = detector.find_faceMesh(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
