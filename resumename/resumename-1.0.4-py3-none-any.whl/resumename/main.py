# encoding=utf-8
# @Author=zhukai@eccom.com.cn
# @Date=2021/10/25
# @Utility: 解析姓名


import re
import os
import logging
import torch
from resumename.model import TextCNN

# logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO)


package_dir = os.path.dirname(os.path.abspath(__file__))


class NameParser(object):
    """ Extract name of resume. """
    def __init__(self, threshold=0.85):
        self.threshold = threshold

        self.surnames = r"\b(" + r"|".join(self.load_xingshi()) + r")" + r"(\s*\w)(\s*\w)?\b"
        logger.info(f"Part of surnames is {self.surnames[:50]}......")

        self.surnames = re.compile(self.surnames)

        self.model = TextCNN()
        self.model.load_state_dict(torch.load(os.path.join(package_dir, "checkpoint", "cnn_20742.pt")))
        logger.info("Loading trained TextCNN successfully.")
        logger.info("Initialization of NameParser have done.")

    def load_xingshi(self):
        """ load most common surname. reference: https://blog.csdn.net/bprl6658/article/details/100949065 """

        surnames = set()
        with open(os.path.join(package_dir, "xingshi.txt"), "rt", encoding="utf-8") as fp:
            for line in fp.readlines():
                if not line.startswith("#"):
                    surnames.add(line.strip())

        return surnames

    def parse(self, content):
        """ content is resume's content. """
        if not content:
            return None

        # extraction by `姓名` flag
        match = re.search(r"(?<!紧急联系人)(姓\s*名\s*[:：]?\s*)(?P<name>\w{2,4})", content)
        if match:
            name = match.group("name").strip()

            name_prob = self.model.predict(f"{name}是有效的姓名。")
            if name_prob >= self.threshold:
                return name

        # extraction by `baijiaxing`
        match = re.search(self.surnames, content)
        if match:
            name = match.group().strip()
            name = re.sub(r"\s*", "", name)

            name_prob = self.model.predict(f"{name}是有效的姓名。")
            if name_prob >= self.threshold:
                return name

        return None


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = os.listdir(os.path.join(root_dir, "boss_txt"))
    print(f"Totally file number is {len(files)}.")

    parser = NameParser()

    with open(os.path.join(root_dir, "result.txt"), "wt") as pri_fp:
        for file in files:
            with open(os.path.join(root_dir, "boss_txt", file), "rt") as fp:
                ct = fp.read().strip()

            print(f"Truth: {file.strip('.txt')}; Predict: {parser.parse(ct)}\n")
            pri_fp.write(f"Truth: {file.strip('.txt')}; Predict: {parser.parse(ct)}\n")
