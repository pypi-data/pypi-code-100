# encoding=utf-8
# @Author=zhukai@eccom.com.cn
# @Date=2021/10/28
# @Utility: 编码汉字


import os
import json


class Tokenizer(object):
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocabulary.json"),
                  "rt", encoding="utf-8") as fp:
            self.vocab = json.load(fp)

        self.token2id = dict([(token, idx) for idx, token in enumerate(self.vocab)])
        self.id2token = dict([(idx, token) for idx, token in enumerate(self.vocab)])

    def tokenize(self, text: str, max_len=11, padding=True):
        default = self.token2id["<UNK>"]
        temp = [self.token2id.get(item, default) for item in text.strip()]

        if padding:
            temp += [self.token2id.get("<PAD>")] * (max_len - len(temp))

        return temp


if __name__ == "__main__":
    pass
