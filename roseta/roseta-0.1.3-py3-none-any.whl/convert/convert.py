import logging
from typing import Tuple
from typing import Union
from typing import Optional

from roseta.utils.data_util import get_config
from roseta.transform.no_class import handle_no_class
from roseta.transform.height import handle_height
from roseta.transform.weight import handle_weight
from roseta.transform.city import handle_city
from roseta.transform.foot import handle_foot

logger = logging.getLogger(__name__)
config = get_config()


def eat(text: str, cls: Optional[str] = None, unit: Optional[str] = None) -> Tuple[Union[int, float, str], str]:
    # 转为小写字母
    text = str(text).lower()

    # 确定正负号
    if text[0] in ["负", "-"]:
        text = text[1:]
        sign = -1
    else:
        sign = 1

    # 确定参数
    if cls is None:
        for key, values in config["cn_unit_check_dict"].items():
            for value in values:
                if value in text:
                    cls = key
                    break
        if cls is None:
            cls = "no"

    if unit is None:
        if cls == "no":
            unit = "no"
        else:
            unit = config["std_unit_check_dict"][cls][0]
    else:
        if cls != "no" and unit not in config["std_unit_check_dict"][cls]:
            raise Exception(f"数据和单位不匹配：{text} | {unit}")

    # 特殊处理
    for key, value in config["spacial_dict"].items():
        if key in text:
            logger.info(f"自动转化「{text}」：{key} -> {value}")
            text = text.replace(key, value)

    if cls == "no":
        text, unit = handle_no_class(text, unit)
    elif cls == "height":
        text, unit = handle_height(text, unit)
    elif cls == "weight":
        text, unit = handle_weight(text, unit)
    elif cls == "city":
        text, unit = handle_city(text, unit)
    elif cls == "foot":
        text, unit = handle_foot(text, unit)
    else:
        raise Exception(f"unknown class: {cls}")

    if type(text) in [int, float]:
        return sign * text, unit
    else:
        return text, unit
