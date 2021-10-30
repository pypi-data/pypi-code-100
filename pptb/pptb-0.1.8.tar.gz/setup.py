# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pptb',
 'pptb.nn',
 'pptb.optimizer',
 'pptb.tools',
 'pptb.utils',
 'pptb.vision',
 'pptb.vision.models']

package_data = \
{'': ['*']}

extras_require = \
{'paddle': ['paddlepaddle>=2.2.0rc0,<3.0.0']}

setup_kwargs = {
    'name': 'pptb',
    'version': '0.1.8',
    'description': '🚣 一些常用的但 paddle 里没有的小工具～',
    'long_description': '# Paddle Toolbox [WIP]\n\n一些方便的小工具，参考 Paddle 的 API 设计以及 Torch Toolbox API 设计\n\n## 安装\n\n### 使用 pip 安装\n\n```bash\npip install pptb\n```\n\n由于仍处于开发阶段，API 较为不稳定，建议安装时指定版本号\n\n```bash\npip install pptb==0.1.8\n```\n\n### 直接从 GitHub 拉取最新代码\n\n这里以 AI Studio 为例\n\n```bash\ngit clone https://github.com/cattidea/paddle-toolbox.git work/paddle-toolbox/\n# 如果下载太慢导致出错请使用下面的命令\n# git clone https://hub.fastgit.org/cattidea/paddle-toolbox.git work/paddle-toolbox/\n```\n\n之后在你的 Notebook 或者 Python 文件中加入以下代码\n\n```python\nimport sys\n\nsys.path.append(\'/home/aistudio/work/paddle-toolbox/\')\n```\n\n## 已支持的工具\n\n### LabelSmoothingLoss\n\n```python\nimport paddle\nfrom pptb.nn import LabelSmoothingLoss\n\nnum_classes = 40\nlabel_smooth_epision = 0.1\n\n# 如果需要标签平滑后 Loss，将下面这行替换成后面那一行即可\n# loss_function = paddle.nn.CrossEntropyLoss()\nloss_function = LabelSmoothingLoss(paddle.nn.CrossEntropyLoss(soft_label=True), num_classes, label_smooth_epision)\n```\n\n### CosineWarmup\n\n```python\nimport paddle\nfrom pptb.optimizer.lr import CosineWarmup\n\n# ...\n\ntrain_batch_size = 32\nlearning_rate = 3e-4\nstep_each_epoch = len(train_set) // train_batch_size\nnum_epochs = 40\nwarmup_epochs = 3\n\nlr_scheduler = CosineWarmup(\n    learning_rate,\n    total_steps = num_epochs * step_each_epoch,\n    warmup_steps = warmup_epochs * step_each_epoch,\n    warmup_start_lr = 0.0,\n    cosine_end_lr = 0.0,\n    last_epoch = -1\n)\n\n```\n\n### Mixup && Cutmix\n\n#### Mixup\n\n```python\nimport paddle\nfrom pptb.tools import mixup_data, mixup_criterion, mixup_metric\n\n# ...\n\nuse_mixup = True\nmixup_alpha = 0.2\n\nfor X_batch, y_batch in train_loader():\n   # 使用 mixup 与不使用 mixup 代码的前向传播部分代码差异对比\n   if use_mixup:\n      X_batch_mixed, y_batch_a, y_batch_b, lam = mixup_data(X_batch, y_batch, mixup_alpha)\n      predicts = model(X_batch_mixed)\n      loss = mixup_criterion(loss_function, predicts, y_batch_a, y_batch_b, lam)\n      acc = mixup_metric(paddle.metric.accuracy, predicts, y_batch_a, y_batch_b, lam)\n   else:\n      predicts = model(X_batch)\n      loss = loss_function(predicts, y_batch)\n      acc = paddle.metric.accuracy(predicts, y_batch)\n\n   # ...\n```\n\n除了用于处理 paddle 里 `Tensor` 的 `mixup_data`，还可以使用 `mixup_data_numpy` 处理 numpy 的 ndarray。\n\n#### Cutmix\n\n和 Mixup 一样，只需要将 `mixup_data` 换为 `cutmix_data` 即可，与 `mixup_data` 不同的是，`cutmix_data` 还接收一个额外参数 `axes` 用于控制需要 mix 的是哪几根 axis，默认 `axes = [2, 3]`，也即 `NCHW` 格式图片数据对应的 `H` 与 `W` 两根 axis。\n\n#### MixingDataController\n\n用于方便管理使用 Mixup 和 Cutmix\n\n```python\nimport paddle\nfrom pptb.tools import MixingDataController\n\n# ...\n\nmixing_data_controller = MixingDataController(\n   mixup_prob=0.3,\n   cutmix_prob=0.3,\n   mixup_alpha=0.2,\n   cutmix_alpha=0.2,\n   cutmix_axes=[2, 3],\n   loss_function=paddle.nn.CrossEntropyLoss(),\n   metric_function=paddle.metric.accuracy,\n)\n\nfor X_batch, y_batch in train_loader():\n   X_batch_mixed, y_batch_a, y_batch_b, lam = mixing_data_controller.mix(X_batch, y_batch, is_numpy=False)\n   predicts = model(X_batch_mixed)\n   loss = mixing_data_controller.loss(predicts, y_batch_a, y_batch_b, lam)\n   acc = mixing_data_controller.metric(predicts, y_batch_a, y_batch_b, lam)\n\n   # ...\n```\n\n### Vision models\n\n提供更加丰富的 backbone，所有模型均会提供预训练权重\n\n已支持一些 PaddleClas 下的预训练模型，以及比较新的 ConvMixer\n\n-  GoogLeNet\n-  Incetpionv3（已并入 paddle 主线）\n-  ResNeXt（已并入 paddle 主线）\n-  ShuffleNetV2\n-  ConvMixer（预训练权重转自 PyTorch）\n-  DenseNet (未完整支持)\n\n```python\nimport paddle\nimport pptb.vision.models as ppmodels\n\nmodel = ppmodels.resnext50_32x4d(pretrained=True)\n```\n\nPS: 如果这些模型无法满足你的需求的话，可以试试囊括了很多比较新的模型的 [ppim](https://github.com/AgentMaker/Paddle-Image-Models)~\n\n#### ConvMixer\n\n| Model Name                | Kernel Size | Patch Size | Top-1                                                 | Top-5  |\n| ------------------------- | ----------- | ---------- | ----------------------------------------------------- | ------ |\n| convmixer_768_32          | 7           | 7          | 0.7974<span style="color:green;"><sub>(-0.0042)</sub> | 0.9486 |\n| convmixer_1024_20_ks9_p14 | 9           | 14         | 0.7681<span style="color:green;"><sub>(-0.0013)</sub> | 0.9335 |\n| convmixer_1536_20         | 9           | 7          | 0.8083<sub><span style="color:green;">(-0.0054)</sub> | 0.9557 |\n\n### TODO List\n\n一些近期想做的功能\n\n-  [x] Cutmix\n-  [ ] Activation、Mish\n-  [ ] ~~Lookahead (paddle.incubate.LookAhead 已经有了)~~\n-  [ ] 更多 vision models\n   -  [ ] MobileNetV3\n   -  [ ] Xception\n   -  [ ] Swin Transformer\n   -  [ ] DenseNet（完整支持）\n-  [ ] 完整的单元测试\n\n## References\n\n-  [PaddlePaddle](https://github.com/PaddlePaddle/Paddle)\n-  [Torch Toolbox](https://github.com/PistonY/torch-toolbox)\n',
    'author': 'Nyakku Shigure',
    'author_email': 'sigure.qaq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cattidea/paddle-toolbox',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
