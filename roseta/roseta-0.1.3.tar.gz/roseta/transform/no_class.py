import re
from typing import Tuple
from typing import Union

from cn2an import cn2an
from cn2an import an2cn
from proces import preprocess

from roseta.utils.log_util import get_logger
from roseta.utils.data_util import get_config

logger = get_logger("roseta.height", "info")
config = get_config()


def trans_no_class(text: str, unit: str) -> Tuple[Union[int, float], str]:
    # 预处理
    text = preprocess(text)

    # 确定正负号
    if text[0] in ["负", "-"]:
        text = text[1:]
        sign = -1
    else:
        sign = 1

    # 处理特殊表示「几、多」
    for key, value in config["spacial_dict"].items():
        if key in text:
            logger.info(f"自动转化「{text}」：{key} -> {value}")
            text = text.replace(key, value)

    cn_num_unit_list = config["cn_num_unit_list"]
    an_num_list = config["an_num_list"]
    cn_num_list = config["cn_num_list"]

    # 零 零点八 八 八十 八十八 负八十八
    result = re.search(f"^[{cn_num_unit_list}]+$", text)
    if result:
        num = cn2an(text, "normal")
    else:
        # 0 0.8 8 80 88 -88
        result = re.search(f"^[{an_num_list}]+$", text)
        if result:
            if "." in text:
                num = float(text)
            else:
                num = int(text)
        else:
            # 80多 80几
            result = re.search(f"^[{an_num_list}]+[{cn_num_list}]$", text)
            if result:
                num_text = an2cn(text[:-1]) + text[-1]
                num = cn2an(num_text)
            else:
                raise Exception(f"！！trans_no_cls 暂时不能处理的文本格式：{text}")

    return sign * num, unit
