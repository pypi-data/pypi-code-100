import requests
import json


class PVWattsAPI:
    BASE_URL = "https://developer.nrel.gov/api/pvwatts/v6"
    PARAMS = {"format": "json",
              "api_key": "0imxmweTxXORuNCMHoN3eZta6vfDcvbmgFyILphe",
              "system_capacity": "100",  # 容量
              "module_type": "0",  # 面板类型
              "losses": "14",  # 系统损失
              "array_type": "1",  # 方阵类型
              "tilt": "0.5",  # 倾斜角
              "azimuth": "180",  # 方位角
              "address": None,  # 地址
              "lat": "31",  # 纬度
              "lon": "121",  # 经度
              "file_id": None,  # climate data file id
              "dataset": "intl",  # climate dataset to use
              "radius": 100,  # 气象站搜索范围（km）
              "timeframe": "hourly",  # 输出频率
              "dc_ac_ratio": 1.2,  # dc:ac
              "gcr": 0.4,  # ground coverage ratio
              "inv_eff": 96,  # 逆变器效率
              "callback": None
              }
    response = None

    def load_params(self, params: dict):
        for k, v in params.items():
            self.PARAMS.update({k: v})

    def run(self):
        r = requests.get(self.BASE_URL, params=self.PARAMS)
        self.response = json.loads(r.text)
        return self.response
