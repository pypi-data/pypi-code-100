from typing import Tuple
from typing import Union
from typing import Optional

from proces import preprocess

from roseta.utils.data_util import get_config
from roseta.utils.log_util import get_logger
from roseta.transform.no_class import trans_no_class
from roseta.transform.height import trans_height
from roseta.transform.weight import trans_weight
from roseta.transform.city import trans_city
from roseta.transform.foot import trans_foot

logger = get_logger("roseta", "debug")
config = get_config()


def transform(text: str, cls: Optional[str] = None, unit: Optional[str] = None) -> Tuple[Union[int, float, str], str]:
    # 预处理
    text = preprocess(text)

    # 确定参数 cls 和 unit
    if cls is None:
        for key, values in config["cn_unit_check_dict"].items():
            for value in values:
                if value in text:
                    cls = key
                    logger.debug(f"「{text}」自动识别 cls 为 {cls}。")
                    break
        if cls is None:
            cls = "no"

    if unit is None:
        if cls == "no":
            unit = "no"
        else:
            unit = config["std_unit_check_dict"][cls][0]
            logger.debug(f"「{text}」使用默认 unit 为 {unit}。")
    else:
        if cls != "no" and unit not in config["std_unit_check_dict"][cls]:
            raise Exception(f"数据和单位不匹配：{text} | {unit}。")

    if cls == "no":
        text, unit = trans_no_class(text, unit)
    elif cls == "height":
        text, unit = trans_height(text, unit)
    elif cls == "weight":
        text, unit = trans_weight(text, unit)
    elif cls == "city":
        text, unit = trans_city(text, unit)
    elif cls == "foot":
        text, unit = trans_foot(text, unit)
    else:
        raise Exception(f"unknown class: {cls}")

    return text, unit
