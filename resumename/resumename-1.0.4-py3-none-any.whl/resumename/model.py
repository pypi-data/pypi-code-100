# encoding=utf-8
# @Author=zhukai@eccom.com.cn
# @Date=2021/10/26
# @Utility: 模型文件

import torch
from torch import nn
import torch.nn.functional as F
from resumename.tokenizer import Tokenizer


class TextCNN(nn.Module):
    def __init__(self, embedding_feature=128):
        """ create TextCNN based torch """
        super(TextCNN, self).__init__()

        self.tokenizer = Tokenizer()
        self.embedding = nn.Embedding(len(self.tokenizer.vocab), embedding_feature)

        self.kernel_sizes = [2, 3, 4]
        self.output_channel = 10

        # 对文本数据做二维卷积
        # input channel always equal 1 in NLP.
        self.conv2s = nn.ModuleList([nn.Conv2d(1, self.output_channel,
                                     kernel_size=(kernel_size, embedding_feature))
                                     for kernel_size in self.kernel_sizes])
        self.dropout = nn.Dropout(0.1)

        # only single item is needed for binary cross entropy.
        self.fc = nn.Linear(self.output_channel * len(self.kernel_sizes), 1)

    @staticmethod
    def conv_and_maxpool(x, conv_layer):
        """
        after embedding, x.shape: (batch_size, seq_len, feature)
        -> x.unsqueeze(1) -> shape: (batch_size, 1, seq_len, feature)
        -> nn.Conv2d(x) -> shape: (batch_size, output_channels, seq_len - kernel_size + 1, 1)
        -> squeeze(3) -> shape: (batch_size, output_channels, seq_len - kernel_size + 1)
        -> max_pool1d -> shape: (batch_size, output_channels, 1)
        -> squeeze(2) -> shape: (batch_size, output_channels)
        """
        x = x.unsqueeze(1)
        x = conv_layer(x)
        x = x.squeeze(3)
        x = F.max_pool1d(x, kernel_size=x.shape[2])
        x = x.squeeze(2)
        return x

    def forward(self, x, labels=None):
        x = self.embedding(x)

        x = torch.cat([self.conv_and_maxpool(x, conv_layer=conv) for conv in self.conv2s], dim=1)
        x = self.dropout(x)
        logit = torch.sigmoid(self.fc(x).squeeze(1))

        if labels is None:
            return logit
        else:
            loss = F.binary_cross_entropy(logit, labels)
            return loss, logit

    def predict(self, text, max_len=11, padding=True):
        """ predict single sample. """
        x = self.tokenizer.tokenize(text, max_len=max_len, padding=padding)
        x = torch.tensor([x], dtype=torch.long)  # Batch Computation Format

        self.eval()
        with torch.no_grad():
            logit = self(x)

        return round(logit[0].item(), 3)


if __name__ == "__main__":
    x = torch.tensor([list(range(10))], dtype=torch.long)
    y = torch.tensor([0], dtype=torch.float)

    cnn = TextCNN()
    print(cnn(x, y))

    # cnn.load_state_dict(torch.load("/home/zhukai/PycharmProjects/ResumeParse/checkpoint/cnn_20742.pt"))
    print(cnn.predict("电话是有效的姓名。"))
