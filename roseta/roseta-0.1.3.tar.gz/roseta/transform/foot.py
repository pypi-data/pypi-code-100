import re
from typing import Tuple
from typing import Union
from typing import Optional

from cn2an import cn2an
from proces import preprocess

from roseta.utils.log_util import get_logger
from roseta.utils.data_util import get_config

logger = get_logger("roseta.height", "info")
config = get_config()


def trans_foot(text: str, unit: Optional[str] = None) -> Tuple[Union[int, float], str]:
    if unit is None:
        unit = config["std_unit_check_dict"]["foot"][0]

    # 预处理
    text = preprocess(text)

    # 处理特殊表示「几、多」
    for key, value in config["spacial_dict"].items():
        if key in text:
            logger.info(f"自动转化「{text}」：{key} -> {value}")
            text = text.replace(key, value)

    an_num_list = config["an_num_list"]
    cn_num_list = config["cn_num_list"]
    all_num = an_num_list + cn_num_list

    # 二尺 两尺 一尺八
    result = re.findall(f"^([{all_num}]" + "{1,3})" + f"尺([{all_num}]"+"{0,2})寸?$", text)
    if len(result) > 0:
        n1, n2 = result[0]
        n1 = cn2an(n1, mode="smart")
        if len(n2) > 0:
            n2 = cn2an(n2, mode="smart")
            chi = float(n1) + float(n2) * (10 ** (-1*len(str(int(n2)))))
        else:
            chi = float(n1)
        num = round(chi*33.3333, 2)
        if unit == "m":
            num = round(num / 100, 4)
    else:
        raise Exception(f"！！trans_foot 暂时不能处理的文本格式：{text}")

    return num, unit
