import grpc
import cv2
from .proto_2 import facerec_pb2
from .proto_2 import facerec_pb2_grpc
import numpy as np
import math
from .facemodel import BaseFaceMoel

class FaceModel(BaseFaceMoel):
    def __init__(self, filename, channel, *, is_full=False):
        super().__init__(filename, channel, is_full=is_full)

        self._features = [] 
        self._load_features()

    def _compute(self, num):
        return math.ceil(num/160)*160

    def _load_features(self):
        
        with self._channel() as ch:
            stub = facerec_pb2_grpc.FaceRecStub(ch)
            img = cv2.imread(self.filename)
            height,width,_ = img.shape

            img_encode = cv2.imencode('.jpg', img)[1]
            img_data = img_encode.tobytes()
            resp = stub.GetFeatures(facerec_pb2.ImageReq(image=img_data, width=640, height=640))
            #ch.close()

            #print(filename, height,width, self._compute(width), self._compute(height), resp.features)
          
            self.height = height
            self.width = width
            self._convert(resp.features)

    def lens(self):
        return len(self._features)

    def _convert(self, features):
        self._features = []
        for feature  in features:
            face = feature.face
            box = [face.x1, face.y1, face.x2, face.y2]
            #print(box)

            if self.is_full==False or (face.x1>0 and face.x2<self.width and face.y1>0 and face.y2<self.height):
                #print(box)
                if (face.x2-face.x1)*(face.y2-face.y1)>=625:
                    feature = np.array([feature.feature])
                    feature = feature/np.linalg.norm(feature)
                    self._features.append((feature, box, face.landmarks, face.confidence))

    def features(self):
        """
        """
        for row  in self._features:
            yield row
