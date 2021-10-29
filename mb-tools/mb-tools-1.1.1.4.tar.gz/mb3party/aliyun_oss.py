import oss2

from mbutils import cfg


class AliyunOSS:
    def __init__(self, oss_config):
        self.access_key_id = oss_config.get("accessKeyId")
        self.access_key_secret = oss_config.get("accessKeySecret")
        self.bucket = oss_config.get("bucket")
        self.region = oss_config.get("region")

    def put_object(self, oss_file, local_file):
        """
        OSS 本地文件上传到oss
        :param oss_file:
        :param local_file:
        :return:
        """
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, 'http://{}.aliyuncs.com'.format(self.region), self.bucket)
        bucket.put_object_from_file('exportFiles/{}'.format(oss_file), local_file)

    def get_object(self, oss_file):
        """
        OSS 文件流下载到本地
        :param oss_file:
        :param local_file:
        :return:
        """
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, 'http://{}.aliyuncs.com'.format(self.region), self.bucket)
        # bucket.get_object_to_file('exportFiles/{}'.format(oss_file), 'template/{}'.format(local_file))
        # 文件流
        object_stream = bucket.get_object('exportFiles/{}'.format(oss_file))
        return object_stream.read()

    def put_object_bytes(self, oss_file, file_bytes):
        """
        OSS bytes上传到oss
        :param oss_file:
        :param local_file:
        :return:
        """
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        bucket = oss2.Bucket(auth, 'http://{}.aliyuncs.com'.format(self.region), self.bucket)
        bucket.put_object('exportFiles/{}'.format(oss_file), file_bytes)


if __name__ == '__main__':
    oss_config = cfg.get("OSSConfig")
    res = AliyunOSS(oss_config)
    # res.put_object('共享系统数据报表-2020-09-15 09:38:31.zip', '共享系统数据报表-2020-09-15 09_38_31.zip')
    # res.get_object('共享系统数据报表-2020-09-15 09:38:31.zip', '共享系统数据报表-2020-09-15 09_38_31.zip')
    object_list = []
    file_list = ["共享系统数据报表-2020-09-21 10:11:51[0].xlsx", "共享系统数据报表-2020-09-21 10:11:51[1].xlsx"]
    for r in file_list:
        object_list.append(res.get_object(r))

    from io import BytesIO
    import zipfile

    in_memory_zip = BytesIO()
    zf = zipfile.ZipFile(in_memory_zip, 'a', zipfile.ZIP_DEFLATED, False)

    for idx, r in enumerate(object_list):
        zf.writestr(file_list[idx], r)

    # 下载到本地
    # in_memory_zip.seek(0)
    # with open('./haha.zip', 'wb') as wf:
    #     wf.write(in_memory_zip.read())
    in_memory_zip.seek(0)
    a = in_memory_zip.read()
    # 上传到oss
    res.put_object_bytes("haha.zip", a)
    print(object_list)
