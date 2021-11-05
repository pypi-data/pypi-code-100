from typing import Tuple
import re
import logging

from cn2an import cn2an
from cn2an import an2cn

logger = logging.getLogger(__name__)

cn_unit_check_dict = {
    "height": ["厘米", "米", "cm", "m"],
    "weight": ["斤", "公斤", "克", "千克", "g", "kg"]
}
std_unit_check_dict = {
    # 第一位为默认
    "height": ["cm", "m"],
    "weight": ["kg", "g"]
}
spacial_dict = {
    "几": "五",
    "多": "二"
}

cn_num_unit_list = "零一壹幺二贰两三叁仨四肆五伍六陆七柒八捌九玖十拾百佰千仟万亿点负"
cn_num_list = "零一壹幺二贰两三叁仨四肆五伍六陆七柒八捌九玖"
an_num_list = "0123456789."


def eat(text, cls=None, unit=None) -> Tuple:
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
        for key, values in cn_unit_check_dict.items():
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
            unit = std_unit_check_dict[cls][0]
    else:
        if cls != "no" and unit not in std_unit_check_dict[cls]:
            raise Exception(f"数据和单位不匹配：{text} | {unit}")

    # 特殊处理
    for key, value in spacial_dict.items():
        if key in text:
            logger.info(f"自动转化「{text}」：{key} -> {value}")
            text = text.replace(key, value)

    if cls == "no":
        num, unit = handle_no_cls(text, unit)
    elif cls == "height":
        num, unit = handle_height(text, unit)
    elif cls == "weight":
        num, unit = handle_weight(text, unit)
    else:
        raise Exception(f"unknown class: {cls}")

    return sign * num, unit


def handle_no_cls(text, unit):
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


def handle_height(text, unit):
    # 八 八十 八十七 八厘米 八十厘米 八十七厘米 八米 八十米 八十七米
    result = re.search(f"^[{cn_num_unit_list}]+(厘米|米|cm|m)?$", text)
    if result:
        if text[-2:] in ["厘米", "cm"]:
            num_text = text[:-2]
            cur_unit = "cm"
        elif text[-1] in ["米", "m"]:
            num_text = text[:-1]
            cur_unit = "m"
        else:
            num_text = text
            cur_unit = unit

        num = cn2an(num_text, "normal")
    else:
        # 8 80 180 8厘米 80厘米 180厘米 8米 80米 180米
        result = re.search(f"^[{an_num_list}]+(厘米|米|cm|m)?$", text)
        if result:
            if text[-2:] in ["厘米", "cm"]:
                num_text = text[:-2]
                cur_unit = "cm"
            elif text[-1] in ["米", "m"]:
                num_text = text[:-1]
                cur_unit = "m"
            else:
                num_text = text
                cur_unit = unit

            if "." in num_text:
                num = float(num_text)
            else:
                num = int(num_text)
        else:
            # 一米八 一米八七 一米8 一米87 1米八 1米八七 1米8 1米87
            result = re.search(f"^[{cn_num_list}{an_num_list}]米[{cn_num_list}{an_num_list}]" + "{1,2}$", text)
            if result:
                num_text_hundred, num_text_other = text.split("米")
                # 处理百位
                if num_text_hundred in cn_num_list:
                    num = cn2an(num_text_hundred, "normal") * 100
                else:
                    num = int(num_text_hundred) * 100
                # 处理十位个位
                if num_text_other[-1] in cn_num_list:
                    if len(num_text_other) == 2:
                        num = num + cn2an(num_text_other, "normal")
                    else:
                        num = num + cn2an(num_text_other, "normal") * 10
                else:
                    if len(num_text_other) == 2:
                        num = num + int(num_text_other)
                    else:
                        num = num + int(num_text_other) * 10
                cur_unit = "cm"
            else:
                # 80多 80多米 80多厘米 80几 80几米 80几厘米
                result = re.search(f"^[{an_num_list}]+[{cn_num_list}](厘米|米|cm|m)?$", text)
                if result:
                    if text[-2:] in ["厘米", "cm"]:
                        num_text = text[:-2]
                        cur_unit = "cm"
                    elif text[-1] in ["米", "m"]:
                        num_text = text[:-1]
                        cur_unit = "m"
                    else:
                        num_text = text
                        cur_unit = unit

                    num = cn2an(an2cn(num_text[:-1]) + num_text[-1])
                else:
                    raise Exception(f"！！handle_height 暂时不能处理的文本格式：{text}")

    # 单位规范化
    if unit == "cm" and cur_unit == "m":
        num = num * 100
    elif unit == "m" and cur_unit == "cm":
        # 处理 0.018 / 100 = 0.00017999999999999998
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num / 100, decimal_len + 2)
        else:
            num = num / 100
    else:
        num = num

    return num, unit


def handle_weight(text, unit):
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
                    raise Exception(f"！！handle_height 暂时不能处理的文本格式：{text}")

    # 单位规范化
    # 处理 斤
    if cur_unit == "jin":
        num = num * 500
        cur_unit = "g"

    if unit == "g" and cur_unit == "kg":
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

    return num, unit
