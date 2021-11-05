import re
import logging
from typing import Tuple
from typing import Union

from cn2an import cn2an
from cn2an import an2cn

from roseta.utils.data_util import get_config

logger = logging.getLogger(__name__)
config = get_config()


def handle_no_class(text: str, unit: str) -> Tuple[Union[int, float], str]:
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
                raise Exception(f"！！handle_no_cls 暂时不能处理的文本格式：{text}")

    return num, unit
