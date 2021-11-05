import re
import logging
from typing import Tuple
from typing import Union

from cn2an import cn2an

from roseta.utils.data_util import get_config

logger = logging.getLogger(__name__)
config = get_config()


def handle_foot(text: str, unit: str) -> Tuple[Union[int, float], str]:
    an_num_list = config["an_num_list"]
    cn_num_list = config["cn_num_list"]
    all_num = an_num_list + cn_num_list

    # 二尺 两尺 一尺八
    result = re.findall(f"^([{all_num}]" + "{1,3})" + f"尺([{all_num}]"+"{0,2})寸?$", text)
    if len(result) > 0:
        n1, n2 = result[0]
        flag = False
        for n in n1:
            if n not in an_num_list:
                flag = True
        if flag:
            n1 = cn2an(n1, mode="smart")

        if len(n2) > 0:
            flag = False
            for n in n2:
                if n not in an_num_list:
                    flag = True
            if flag:
                n2 = cn2an(n2, mode="smart")
        else:
            n2 = 0

        num = round((float(n1) + float(n2) * (10 ** (len(str(n2))*-1)))*33.3333, 2)

        if unit == "m":
            num = num / 100
    else:
        raise Exception(f"！！handle_height 暂时不能处理的文本格式：{text}")

    return num, unit
