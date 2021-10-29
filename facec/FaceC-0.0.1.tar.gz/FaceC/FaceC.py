import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection()

    def findFace(self, frame, draw=True):

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                if draw:
                    self.fancyDraw(frame, bbox)
                    cv2.putText(frame, f"{int(detection.score[0]*100)}%", (bbox[0], bbox[1]-20),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return bboxs

    def fancyDraw(self, frame, bbox, l=30, t=5, rt=1):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(frame, bbox, (255, 0, 255), rt)
        # Top Left
        cv2.line(frame, (x, y), (x+l, y), (255, 0, 255), t)
        cv2.line(frame, (x, y), (x, y+l), (255, 0, 255), t)
        # Top Right
        cv2.line(frame, (x1, y), (x1-l, y), (255, 0, 255), t)
        cv2.line(frame, (x1, y), (x1, y+l), (255, 0, 255), t)
        # Bottom Left
        cv2.line(frame, (x, y1), (x+l, y1), (255, 0, 255), t)
        cv2.line(frame, (x, y1), (x, y1-l), (255, 0, 255), t)
        # Bottom Right
        cv2.line(frame, (x1, y1), (x1-l, y1), (255, 0, 255), t)
        cv2.line(frame, (x1, y1), (x1, y1-l), (255, 0, 255), t)
        return(frame)

    def showImage(self, key, frameName="Frame"):
        cap = cv2.VideoCapture(0)
        pTime = 0
        detector = FaceDetector()
        while True:
            ret, frame = cap.read()
            bboxs = detector.findFace(frame)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(
                frame, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
            cv2.imshow(frameName, frame)
            if cv2.waitKey(1) & 0xFF == ord(key):
                break
        cap.release()
        cv2.destroyAllWindows


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True:
        ret, frame = cap.read()
        bboxs = detector.findFace(frame)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            frame, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows


if __name__ == "__main__":
    main()
