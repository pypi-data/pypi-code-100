import json
import fc2


class AliyunFunc:
    def __init__(self, account_id, region, access_key_id, access_key_secret, service_name, function_name, body,
                 path=""):
        """
         调用函数计算，执行 HTTP 触发器函数
        :param account_id:
        :param region:
        :param access_key_id:
        :param access_key_secret:
        :param service_name:
        :param function_name:
        :param path:
        :param body:
        """
        self.client = fc2.Client(
            endpoint='http://{0}.{1}.fc.aliyuncs.com'.format(account_id, region),
            accessKeyID=access_key_id,
            accessKeySecret=access_key_secret,
            Timeout=61 * 60
        )
        self.service_name = service_name
        self.function_name = function_name
        self.path = path
        self.body = json.dumps(body, ensure_ascii=False)

    def do_http_request(self):
        return self.client.do_http_request(
            method="post",
            serviceName=self.service_name,
            functionName=self.function_name,
            path=self.path,
            headers={},
            body=bytes(self.body, encoding="utf8")
        )


if __name__ == '__main__':
    # xibaoda config
    res = AliyunFunc(account_id="1841982702690546",
                     region="cn-shenzhen",
                     access_key_id="LTAI4FwWZJjNGeabTzCDgXmB",
                     access_key_secret="fWbyZq7kLKdKHtYzlK3B0dtVcUTRvx",
                     service_name="script4py",
                     function_name="dashboardReport",
                     body={"start_time": 1563206400000, "end_time": 1564675199000,
                           "file_name": "共享系统数据报表-2020-05-28 20:34:33"
                           }
                     )
    req = res.do_http_request()
    print(req)
