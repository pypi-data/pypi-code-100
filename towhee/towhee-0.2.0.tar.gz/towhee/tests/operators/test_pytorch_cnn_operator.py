# Copyright 2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

from pathlib import Path

from PIL import Image

from towhee.tests.mock_operators import PYTORCH_CNN_OPERATOR_PATH, load_local_operator
from towhee.tests.mock_operators.pytorch_transform_operator.pytorch_transform_operator import PytorchTransformOperator

cache_path = Path(__file__).parent.parent.resolve()
test_image = cache_path.joinpath('data/dataset/kaggle_dataset_small/train/001cdf01b096e06d78e9e5112d419397.jpg')


class TestOperator(unittest.TestCase):
    """
    Simple operator test
    """
    def setUp(self) -> None:
        img_pil = Image.open(test_image)
        op = PytorchTransformOperator(256)
        self.img_tensor = op(img_pil).img_transformed
        self.model = 'resnet50'

    def test_func_operator(self):
        pytorch_cnn_operator = load_local_operator(
            'pytorch_cnn_operator', PYTORCH_CNN_OPERATOR_PATH)
        op = pytorch_cnn_operator.PytorchCnnOperator(self.model)
        self.assertEqual((1, 1000), op(self.img_tensor)[0].shape)


if __name__ == '__main__':
    unittest.main()
