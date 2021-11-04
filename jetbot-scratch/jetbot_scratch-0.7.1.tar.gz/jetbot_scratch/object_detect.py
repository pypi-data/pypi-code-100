import cv2
import jetson.inference
import numpy as np
from numpy import linalg as LA
import os


class ObjectDetector():
    def __init__(self) -> None:
        self.net = jetson.inference.detectNet('ssd-mobilenet-v2')
        x = np.ones((224, 224, 3))
        cuda_mem = jetson.utils.cudaFromNumpy(x)
        self.net.Detect(cuda_mem)
        del cuda_mem
        self.target = 'None'
        cur_dir = os.path.split(os.path.realpath(__file__))[0]
        path_to_labels = os.path.join(cur_dir, 'ssd_coco_labels.txt')
        label_list = []
        self.label_map_dict = {}
        with open(path_to_labels, 'r') as f:
            label_list = [line[:-1] for line in f]
            self.label_map_dict = {v: i for i, v in enumerate(label_list)}
        self.label_map_dict['None'] = 999
        self.height = 360
        self.width = 640

    def detect(self, frame):
        self.height, self.width = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cuda_mem = jetson.utils.cudaFromNumpy(rgb)
        detections = self.net.Detect(cuda_mem)
        res = jetson.utils.cudaAllocMapped(width=cuda_mem.width,
                                           height=cuda_mem.height,
                                           format='bgr8')
        jetson.utils.cudaConvertColor(cuda_mem, res)
        jetson.utils.cudaDeviceSynchronize()
        frame[:] = jetson.utils.cudaToNumpy(res)[:]
        return detections

    def set_target(self, target):
        if target not in self.label_map_dict.keys():
            self.target = 'None'
        else:
            self.target = target

    def get_target_location(self, detections):
        centers = []
        for detection in detections:
            if self.label_map_dict[
                    self.
                    target] == detection.ClassID and detection.Confidence > 0.5:
                centers.append(detection.Center)
        return self.closest_detection(centers)

    def closest_detection(self, centers):
        closest_detection = (0, 0)
        ret = False
        min_distance = 100
        for c in centers:
            cn = [c[0] / self.width * 2 - 1, c[1] / self.height * 2 - 1]
            distance = LA.norm(cn)
            if not ret:
                closest_detection = cn
                min_distance = distance
                ret = True
            elif distance < min_distance:
                closest_detection = cn
                min_distance = distance
        return ret, closest_detection[0], closest_detection[1]
