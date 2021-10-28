from typing import Union, Optional, Sized, Callable, List
from time import time

import torch
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DataLoader, random_split, Dataset, Subset
from torch import Generator

from torch_lib.utils.optim import get_optimizer
from torch_lib.utils.lr_decay import get_scheduler
from torch_lib.utils.metrics import compute_metrics, parse_metrics
from torch_lib.utils import dict_merge, get_device, to_number, func_call, get_dtype, cast, type_check, time_format, list_to_str, execute_batch, unpack
from torch_lib.log.warning import cast_warning
from torch_lib.log.info import device_info, PlainInfo
from torch_lib.log import color_format, progress


def fit(
        model: Module,
        train_dataset: Union[DataLoader, Callable],
        epochs: int,
        metrics: List[Union[str, Module, Callable]],
        optimizer: Union[str, Optimizer] = 'adam',
        learning_rate: float = 1e-4,
        lr_decay=None,
        val_dataset: Union[DataLoader, Callable, None] = None,
        optimizer_options: Optional[dict] = None,
        lr_decay_options: Optional[dict] = None,
        epoch_callbacks: Optional[list] = None,
        step_callbacks: Optional[list] = None
):
    """
    最最最核心的训练函数，训练使用的设备由模型所在设备决定:cpu/cuda
    :param model: 训练的模型
    :param train_dataset: 训练数据集
    :param epochs: 需要训练多少个epochs
    :param optimizer: 优化器，可以自己实例化一个优化器（Optimizer），也可以传入优化器的名字（str）
    :param metrics: 评估指标，一个列表，可以用字符串表示评估指标的名字，也可以传入函数
    :param learning_rate: 学习率，默认1e-4
    :param lr_decay: 学习率衰减，同样的，可以传入字符串或者lr_scheduler的实例
    :param val_dataset: 验证集
    :param optimizer_options: 优化器配置，与optimizer搭配使用，为None则使用pytorch的默认配置（仅当optimizer为字符串时生效）
    :param lr_decay_options: 学习率衰减的配置，与损失函数配置和优化器配置同理
    :param epoch_callbacks: 每一个epoch结束的回调函数（还没开发）
    :param step_callbacks: 每一个training step结束的回调函数（还没开发）
    :return: None
    """
    # 检查模型所在设备
    device = get_device(model)
    dtype = get_dtype(model)
    # 输出设备日志
    device_info.info(device)
    # 控制台输出控制流
    console = PlainInfo(True)
    # 检查数据集是否是函数类型
    train_provider = type_check(train_dataset, Callable, None)
    val_provider = type_check(val_dataset, Callable, None)
    # 转化metrics，并且确定损失函数
    metrics = parse_metrics(metrics, device, dtype, loss_first=True)
    loss_func = metrics[0][0]
    # 初始化优化器
    optimizer_options = dict_merge({
        'lr': learning_rate,
        'params': model.parameters()
    }, optimizer_options)
    optimizer = get_optimizer(optimizer, optimizer_options)
    # 初始化学习率衰减调度器
    lr_decay_options = dict_merge({
        'optimizer': optimizer
    }, lr_decay_options)
    scheduler = get_scheduler(lr_decay, lr_decay_options)
    # 计算总training steps
    total_steps = len(train_dataset)
    # 返回一个计算平均metrics的函数（用于训练集的训练过程展示）
    avg_metrics, clear_metrics = _average_metrics()

    # epoch循环
    for i in range(epochs):
        console.info('epoch', i + 1)
        # 根据epoch动态获取数据集，适用于渐进式学习
        if train_provider is not None:
            del train_dataset
            train_dataset = train_provider(i + 1)
        if val_provider is not None:
            del val_dataset
            val_dataset = val_provider(i + 1)

        # 切换到训练模式
        model.train()

        avg_train_metrics = {}
        # batch循环
        for step, data in enumerate(train_dataset):
            x, y_true = unpack(data, 2)
            # 记录开始时间
            start_time = time()
            # 需要类型转换则警告
            cast_warning.warn(get_dtype(x), dtype)
            # 前向传播
            y_pred = model(cast(x, device, dtype))
            # 设备转换
            y_true = cast(y_true, device)
            # 计算损失
            loss = loss_func(y_pred, y_true)
            # 清除梯度
            optimizer.zero_grad()
            # 反向传播
            loss.backward()
            # 梯度更新
            optimizer.step()
            # 这个batch计算得到的metrics
            train_metrics = compute_metrics(y_pred, y_true, metrics)
            # 释放资源
            del y_pred, y_true
            # 计算这个epoch上的平均metrics
            avg_train_metrics = avg_metrics(train_metrics, step + 1)
            # 执行step_callbacks回调函数
            step_data = {
                'metrics': avg_train_metrics,
                'step': step,
                'total_steps': total_steps,
                'model': model
            }
            execute_batch(step_callbacks, step_data)

            # 记录结束时间
            end_time = time()
            # 控制台训练过程可视化
            console.info(_visualize(step + 1, total_steps, avg_train_metrics, end_time - start_time), mode='r')

        # 学习率衰减
        if scheduler is not None:
            scheduler.step()
        epoch_metrics = avg_train_metrics
        # 验证集验证
        if val_dataset:
            val_metrics = evaluate(model, val_dataset, metrics, console_print=False, val=True)
            epoch_metrics = dict_merge(epoch_metrics, val_metrics)
            console.info(_visualize(total_steps, total_steps, epoch_metrics), mode='r')
        # 执行epoch_callbacks回调函数
        epoch_data = {
            'metrics': epoch_metrics,
            'model': model,
            'epoch': i,
            'total_epochs': epochs
        }
        execute_batch(epoch_callbacks, epoch_data)
        # 清除这一epoch的平均metrics，用于计算下一个epoch的平均metrics（如果不清除的话会导致结果累加错误）
        clear_metrics()
        console.info()


def evaluate(
        model: Module,
        dataset: DataLoader,
        metrics: list,
        console_print: bool = True,
        val: bool = False
):
    """
    模型评估
    :param model: 模型
    :param dataset: 数据集
    :param metrics: 评估指标
    :param console_print: 是否将预测进度展示在控制台
    :param val: 是否是验证集
    :return: 评估指标的字典（如： { 'loss': 0.123456, 'acc': 0.985612 }）
    """
    # 获取模型所在的设备及数据类型
    device = get_device(model)
    dtype = get_dtype(model)
    # 输出设备日志
    device_info.info(device)
    metrics = parse_metrics(metrics, device, dtype)
    return _forward(model, dataset, 'evaluate', console_print, metrics, val)


def predict(model: Module, dataset: DataLoader, console_print: bool = True):
    """

    :param model: 模型
    :param dataset: 数据集
    :param console_print: 是否将推断进度显示在控制台
    :return: 返回结果的预测值和真实值
    """
    # 获取模型所在的设备及数据类型
    device = get_device(model)
    # 输出设备日志
    device_info.info(device)
    return _forward(model, dataset, 'predict', console_print)


def traverse(model: Module, dataset: DataLoader, callbacks: list, metrics: Optional[list] = None, console_print: bool = True, val: bool = False):
    """

    :param model: 模型
    :param dataset: 数据集
    :param callbacks: 批量预测过程中的回调函数
    :param metrics: 遍历时计算评估指标
    :param console_print: 是否将推断进度显示在控制台
    :param val: 是否是验证集
    :return: None
    """
    # 获取模型所在的设备及数据类型
    device = get_device(model)
    dtype = get_dtype(model)
    metrics = parse_metrics(metrics, device, dtype)
    return _forward(model, dataset, 'traverse', console_print, metrics=metrics, callbacks=callbacks, val=val)


def pack(dataset: Dataset, ratios: Optional[list] = None, random: bool = True, generator: Optional[Generator] = None, options: Union[dict, list, None] = None):
    """
    数据集分割以及打包成DataLoader
    :param dataset: 数据集
    :param ratios: 分割比例
    :param random: 随机分割还是顺序分割
    :param generator: 随机分割的种子
    :param options: DataLoader选项
    :return:
    """
    ratios = [1.0] if ratios is None else ratios
    assert sum(ratios) == 1.0, 'the sum of ratios must equals to one'
    assert min(ratios) >= 0, 'ratios must be no less than 0'
    assert hasattr(dataset, '__len__') or isinstance(dataset, Sized), 'dataset has no attr: __len__'

    # 判断dataloader_options是否是list
    list_options = isinstance(options, list)
    if list_options:
        assert len(options) == len(ratios), 'dataloader_options must either be a list and be the same size of ratios or be a dict'

    data_len = len(dataset)
    lengths = [int(round(ratio * data_len)) for ratio in ratios]
    lengths[-1] = data_len - sum(lengths[0:-1])

    if random is False:
        split_data = []
        indices = list(range(data_len))
        index = 0
        for length in lengths:
            split_data.append(Subset(dataset, indices[index:index + length]))
            index += length
    elif generator is None:
        split_data = random_split(dataset, lengths)
    else:
        split_data = random_split(dataset, lengths, generator)

    return tuple((func_call(DataLoader, [split_data[i]], options[i] if list_options else options) for i in range(len(ratios))))


def _visualize(step: int, total_steps: int, metrics: Optional[dict] = None, step_time: Optional[float] = None, progress_len: int = 25):
    """
    控制台可视化，像keras一样可视化训练过程，我最喜欢的部分，因为看起来很酷
    :param step: 当前训练step
    :param total_steps: 总training steps
    :param metrics: 评估指标，这里传入评估指标的字典，用于控制台展示
    :param step_time: 进行一个step所消耗的时间，用于计算ETA
    :param progress_len: 进度条长度（值为25代表将训练过程分成25个小格展示进度，依此类推，基本可以不用动）
    :return: 用于可视化的格式化字符串
    """

    def format_metric(name: str, item: float):
        return '%s: %f  ' % (name, item)

    info = ''

    # 展示评估指标
    if metrics is not None:
        for key, value in metrics.items():
            info += format_metric(key, value)

    return progress(step, total_steps, info, step_time=step_time, progress_len=progress_len, output=False)


def _average_metrics():
    """

    :return:
    """
    metric_dict = {}

    def compute_avg(metrics: Optional[dict], step: int = 1):
        temp = {}
        if metrics is None:
            return temp
        for key, value in metrics.items():
            if key in metric_dict.keys():
                metric_dict[key] += value
            else:
                metric_dict[key] = value
            temp[key] = metric_dict[key] / step
        return temp

    def clear_metrics():
        metric_dict.clear()

    return compute_avg, clear_metrics


def _forward(
        model: Module,
        dataset: DataLoader,
        mode: str,
        console_print: bool = True,
        metrics: list = None,
        val: bool = False,
        callbacks: Optional[list] = None
):
    # 切换到预测模式
    model.eval()
    # 获取模型所在的设备及数据类型
    device = get_device(model)
    dtype = get_dtype(model)
    # 输出设备日志
    device_info.info(device)
    # 控制台输出流
    console = PlainInfo(console_print)

    """
    evaluate_mode = False
    """
    # 用于拼接所有结果
    y_pred_total = []

    """
    evaluate_mode = True
    """
    # 获取模型的steps
    total_steps = len(dataset)
    # 评估指标平均函数
    compute_avg, _ = _average_metrics()
    # 评估指标
    metrics_result = {}

    console.info('predicting...')
    with torch.no_grad():
        for step, data in enumerate(dataset):
            x, y_true = unpack(data, 2)
            # 记录开始时间
            start_time = time()
            # 需要类型转换则警告
            cast_warning.warn(get_dtype(x), dtype)
            # 前向传播
            y_pred = model(cast(x, device, dtype))
            # 设备转换
            y_true = cast(y_true, device)
            # 评估模式计算评估指标
            if mode == 'evaluate':
                metrics_result = compute_avg(compute_metrics(y_pred, y_true, metrics, val), step + 1)
            # 推断模式将结果拼接
            elif mode == 'predict':
                y_pred_total += y_pred
            elif mode == 'traverse':
                _metrics = compute_metrics(y_pred, y_true, metrics, val)
                step_data = {
                    'step': step,
                    'y_pred': y_pred,
                    'y_true': y_true,
                    'metrics': _metrics
                }
                execute_batch(callbacks, step_data)
            del y_pred, y_true
            # 记录结束时间
            end_time = time()
            # 如果设置了控制台打印输出，则显示当前预测进度
            console.info(_visualize(step + 1, total_steps, step_time=end_time - start_time), mode='r')
    console.info()

    if mode == 'evaluate':
        return metrics_result
    elif mode == 'predict':
        return cast(torch.stack(y_pred_total), device, dtype)
