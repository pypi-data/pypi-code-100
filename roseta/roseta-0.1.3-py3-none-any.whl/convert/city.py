import re
import logging
from typing import Tuple
from typing import Union

from roseta.utils.data_util import get_config
from roseta.utils.data_util import get_all_city

logger = logging.getLogger(__name__)
config = get_config()


def handle_city(text: str, unit: str) -> Tuple[Union[int, float], str]:
    all_city = get_all_city()
    city_shi_list = []
    # 特别行政区
    city_special_list = []
    for city_item in all_city:
        city_name = city_item.split("/")[-1]
        if city_name[-1] == "市":
            city_shi_list.append(city_name[:-1])
        else:
            city_special_list.append(city_name[:-5])

    city_shi = "|".join(city_shi_list)
    city_special = "|".join(city_special_list)

    # 杭州 杭州市
    result = re.search(f"^((({city_shi})市?)|({city_special})(特别行政区)?)$", text)
    if result:
        if text[-1] != "市":
            text = text + "市"
    else:
        raise Exception(f"！！handle_city 暂时不能处理的文本格式：{text}")

    if unit == "省":
        for province_city in all_city:
            if text in province_city:
                province_city_list = province_city.split("/")
                text = province_city_list[1] + province_city_list[3]

    return text, unit
