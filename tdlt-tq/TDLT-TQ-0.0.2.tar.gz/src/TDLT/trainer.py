"""
trainer.py文件包含高度封装的trainer。
"""
import time
import torch


class Trainer:
    def __init__(self, /, model, data_loader: dict, optimizer, criterion, epochs: int, device: str):
        super(Trainer, self).__init__()
        self.model = model
        self.train_loader = data_loader['train_loader']
        self.train_num = data_loader['train_num']
        self.val_loader = data_loader['val_loader']
        self.val_num = data_loader['val_num']
        self.optimizer = optimizer
        self.criterion = criterion
        self.epochs = epochs
        self.device = torch.device(device)

    def train(self):
        # 开始训练
        for epoch in range(self.epochs):
            print('epoch {}'.format(epoch + 1))
            time_start = time.time()
            # 训练
            self.model.train()
            train_loss, train_corr = 0.0, 0
            for i, (x, y) in enumerate(self.train_loader):
                # 计算设备
                x = x.to(self.device)
                y = y.to(self.device)
                self.model = self.model.to(self.device)
                # 正向传播
                out = self.model(x)  # 喂数据
                predict_y = torch.max(out, 1)[1]  # 计算预测
                loss = self.criterion(out, y)  # 计算loss
                # 累加loss、correct
                train_loss += loss.item()  # 累加train loss
                train_corr += (predict_y == y).sum().item()  # 累加正确数量
                # 反向传播，更新网络
                self.optimizer.zero_grad()  # 梯度归零
                loss.backward()  # 更新梯度
                self.optimizer.step()  # 更新网络参数
            time_end = time.time()
            print('[TRAIN] epoch:{}/{}, time:{:.2f}s, train_acc:{:.16%}, train_loss:{}, train_corr:{}'
                  .format(epoch, self.epochs, time_end - time_start, train_corr / self.train_num,
                          train_loss / self.train_num, train_corr))

            # 验证
            self.model.eval()
            with torch.no_grad():  # 或者@torch.no_grad() 被他们包裹的代码块不需要计算梯度， 也不需要反向传播
                time_start = time.time()
                val_loss, val_acc, val_corr = 0.0, 0.0, 0
                for i, (x, y) in enumerate(self.val_loader):
                    out = self.model(x)
                    predict_y = torch.max(out, 1)[1]
                    loss = self.criterion(out, y)
                    val_loss += loss.item()
                    val_corr += (predict_y == y).sum().item()
                    time_end = time.time()

                print('[EVAL] time:{:.2f}s, val_acc:{:.16%}, val_loss:{}, val_corr:{}'
                      .format(time_end - time_start, val_corr / self.val_num, val_loss / self.val_num, val_corr))
