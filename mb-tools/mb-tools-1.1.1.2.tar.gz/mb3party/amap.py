import requests


class Amap:
    def __init__(self):
        """
         高德api
        """
        self.key = "a7c6770f7b34521db9689f161a2c8fe7"
        self.base_url = "https://restapi.amap.com"

    def do_direction(self, origin, destination, size=2, mode=1):
        """
        路径规划
        :param origin:出发点经纬度 填入规则：X,Y，采用","分隔，例如“117.500244, 40.417801”
        :param destination:目的地经纬度 填入规则：X,Y，采用","分隔，例如“117.500244, 40.417801”
        :param size: 货车车辆大小 1：微型车，2：轻型车（默认值），3：中型车，4：重型车
        :param mode: 1：骑行路径规划 2：货车路径规划
        :return: distance 起终点的骑行距离(m)  duration 耗时(s)
        """
        if mode == 1:
            url_format = {"base_url": self.base_url, "version": "v4", "model": "direction", "func": "bicycling"}
            params = {"origin": origin, "destination": destination, "key": self.key}
        elif mode == 2:
            url_format = {"base_url": self.base_url, "version": "v4", "model": "direction", "func": "truck"}
            # 如果只需要使用结果中的距离、时间字段，建议设置nosteps=1，可以大幅度提升性能。1
            params = {"size": size, "origin": origin, "destination": destination, "key": self.key, "nosteps": 1}
        else:
            url_format = {"base_url": self.base_url, "version": "v4", "model": "direction", "func": "bicycling"}
            params = {"origin": origin, "destination": destination, "key": self.key}
        url = "{base_url}/{version}/{model}/{func}".format(**url_format)
        response = requests.get(url=url, params=params)
        r_json = response.json()
        try:
            if r_json["errcode"] == 0:
                distance, duration = 0, 0
                if mode == 1:
                    distance = r_json["data"]["paths"][0]["distance"]
                    duration = r_json["data"]["paths"][0]["duration"]
                elif mode == 2:
                    distance = r_json["data"]["route"]["paths"][0]["distance"]
                    duration = r_json["data"]["route"]["paths"][0]["duration"]
                return distance, duration
            else:
                return -1, -1
        except:
            return -1, -1


if __name__ == '__main__':
    res = Amap()

    # 骑行行驶路线
    # https://restapi.amap.com/v4/direction/bicycling?origin=116.481499,39.990475&destination=116.465063,39.999538&key=a7c6770f7b34521db9689f161a2c8fe7
    bicycling_rep = res.do_direction(origin="116.481499,39.990475", destination="116.465063,39.999538", mode=1)

    # 货车行驶路线
    # https://restapi.amap.com/v4/direction/truck?width=2.5&strategy=5&size=2&weight=10&axis=2&origin=116.481008%2C39.989625&destination=116.414217%2C40.061741&height=1.6&load=0.9&key=a7c6770f7b34521db9689f161a2c8fe7&nosteps=1
    truck_rep = res.do_direction(origin="116.481008,39.989625", destination="116.414217,40.061741", size=2, mode=2)
    print(bicycling_rep, truck_rep)
