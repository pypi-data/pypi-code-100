import cv2
import mediapipe as mp
import numpy as np


class SelfieSegmentation:
    def __init__(self):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

        self.mp_draw = mp.solutions.drawing_utils

    def im_segmentation(self, img):
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
        self.results = self.selfie_segmentation.process(img_rgb)

        BG_COLOR = (0, 255, 0)  # gray
        bg_image = cv2.imread('C:/Users/praso/Downloads/1.jpg')

        # Draw selfie segmentation on the background image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack(
            (self.results.segmentation_mask,) * 3, axis=-1) > 0.5
        # The background can be customized.
        #   a) Load an image (with the same width and height of the input image) to
        #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
        #   b) Blur the input image by applying image filtering, e.g.,
        #      bg_image = cv2.GaussianBlur(image,(55,55),0)
        if bg_image is None:
            bg_image = np.zeros(img.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
        output_image = np.where(condition, img, bg_image)

        return output_image


def main():
    cap = cv2.VideoCapture(0)
    detector = SelfieSegmentation()
    while True:
        success, img = cap.read()
        img = detector.im_segmentation(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
