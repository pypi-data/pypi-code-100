import sys
import torch


def check_pypath():
    """
    检查当前解释器地址、虚拟环境名字
    """
    path = sys.executable
    print(f'path : {path}')


def check_cuda():
    print('Cuda Version : ', torch.version.cuda, '\n',
          'Cuda Available : ', torch.cuda.is_available(), '\n',
          'All Device : ', torch.cuda.get_device_name(), '\n',
          'Current Device : ', torch.cuda.current_device(), '\n',
          r"you can use : device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')",
          sep='')
