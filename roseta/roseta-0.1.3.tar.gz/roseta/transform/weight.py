import re
from typing import Tuple
from typing import Union
from typing import Optional

from cn2an import cn2an
from cn2an import an2cn
from proces import preprocess

from roseta.utils.log_util import get_logger
from roseta.utils.data_util import get_config

logger = get_logger("roseta.height", "info")
config = get_config()


def trans_weight(text: str, unit: Optional[str] = None) -> Tuple[Union[int, float], str]:
    if unit is None:
        unit = config["std_unit_check_dict"]["weight"][0]

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

    # 八十 八十斤 八十公斤 八十克 八十千克 八十八斤 八十八公斤 八十八克 八十八千克 八十八g 八十八kg
    result = re.search(f"^[{cn_num_unit_list}]+(斤|公斤|克|千克|g|kg)?$", text)
    if result:
        if text[-2:] in ["公斤", "千克", "kg"]:
            num_text = text[:-2]
            cur_unit = "kg"
        elif text[-1] in ["克", "g"]:
            num_text = text[:-1]
            cur_unit = "g"
        elif text[-1] == "斤":
            num_text = text[:-1]
            cur_unit = "jin"
        else:
            num_text = text
            cur_unit = unit

        num = cn2an(num_text, "normal")
    else:
        # 8 80 180 8斤 8公斤 8克 8千克 80斤 80公斤 80克 80千克 80g 80kg
        result = re.search(f"^[{an_num_list}]+(斤|公斤|克|千克|g|kg)?$", text)
        if result:
            if text[-2:] in ["公斤", "千克", "kg"]:
                num_text = text[:-2]
                cur_unit = "kg"
            elif text[-1] in ["克", "g"]:
                num_text = text[:-1]
                cur_unit = "g"
            elif text[-1] == "斤":
                num_text = text[:-1]
                cur_unit = "jin"
            else:
                num_text = text
                cur_unit = unit

            if "." in num_text:
                num = float(num_text)
            else:
                num = int(num_text)
        else:
            # 一斤八 一斤8 1斤八 1斤8
            result = re.search(f"^[{cn_num_list}{an_num_list}]斤[{cn_num_list}{an_num_list}]$", text)
            if result:
                num_text_hundred, num_text_other = text.split("斤")
                # 处理斤位
                if num_text_hundred in cn_num_list:
                    num = cn2an(num_text_hundred, "normal") * 500
                else:
                    num = int(num_text_hundred) * 500
                # 处理两位
                if num_text_other in cn_num_list:
                    num = num + cn2an(num_text_other, "normal") * 50
                else:
                    num = num + int(num_text_other) * 50

                cur_unit = "g"
            else:
                # 80多 80多斤 80多公斤 80多克 80多千克 80多g 80多kg 80几...
                result = re.search(f"^[{an_num_list}]+[{cn_num_list}](斤|公斤|克|千克|g|kg)?$", text)
                if result:
                    if text[-2:] in ["公斤", "千克", "kg"]:
                        num_text = text[:-2]
                        cur_unit = "kg"
                    elif text[-1] in ["克", "g"]:
                        num_text = text[:-1]
                        cur_unit = "g"
                    elif text[-1] == "斤":
                        num_text = text[:-1]
                        cur_unit = "jin"
                    else:
                        num_text = text
                        cur_unit = unit

                    num_text = an2cn(num_text[:-1]) + num_text[-1]
                    num = cn2an(num_text)
                else:
                    raise Exception(f"！！trans_weight 暂时不能处理的文本格式：{text}")

    # 单位规范化
    # 处理 斤
    if cur_unit == "jin":
        num = num * 500
        cur_unit = "g"

    if unit == "g" and cur_unit == "kg":
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num * 1000, decimal_len - 3)
        else:
            num = num * 1000
    elif unit == "kg" and cur_unit == "g":
        # 处理 0.18 / 1000 = 0.00017999999999999998
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num / 1000, decimal_len + 3)
        else:
            num = num / 1000
    else:
        num = num

    return sign * num, unit
