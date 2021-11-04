import cv2
import torch
import PIL.Image
from torch2trt import TRTModule
from fro_AI.utils.data_utils import get_file, get_hash_prefix_from_file_name
import torch.nn.functional as F
import torchvision.transforms as transforms

model_url = 'http://gz.chuangfeigu.com:8087/fro_AI/models/ObstacleClassifier/obstacle_trt_9b29e551.pth'

device = torch.device('cuda')

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda().half()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda().half()


def preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device).half()
    image = transforms.functional.resize(image, [224, 224])
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]  # 增加一个维度


class ObstacleClassifier():
    def __init__(self) -> None:
        self.model = TRTModule()
        fname = 'obstacle_trt_70fbe733.pth'
        hash_prefix = get_hash_prefix_from_file_name(fname)
        model_path = get_file(fname,
                              model_url,
                              hash_prefix=hash_prefix,
                              cache_subdir='models/ObstacleClassifier')
        self.model.load_state_dict(torch.load(model_path))
        x = torch.ones(1, 1, 224, 224).cuda().half()
        self.model(x)

    def predict(self, frame):
        """predict block or free

        Parameters
        ----------
        frame : np.ndarray
            bgr picture

        Returns
        -------
        float
            1: blocked; 0: free
        """
        x = preprocess(frame)
        y = self.model(x)
        y = F.softmax(y, dim=1)
        return float(y.flatten()[0])
