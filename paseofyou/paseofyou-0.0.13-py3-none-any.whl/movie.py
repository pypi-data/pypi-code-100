class movie:
    def __init__(self, my_movie):
        self.my_movie = my_movie
        self.get()
        self.name = None
        self.url = None
        self.key = None

    def get(self):
        import requests
        from lxml import etree
        try:
            # https://x.wxbxkx.com/
            # http://xue.lxxh.cc/
            url = "http://x.wxbxkx.com//?s={}".format(str(self.my_movie))
            header_ = {
                "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.54_r849063.501 NetType/WIFI"
            }
            req = requests.get(url, headers=header_)
            tree = etree.HTML(req.content.decode("utf-8"))
            if tree.xpath("/html/body/div/main/article[1]/div/header/h2/a//@href"):
                urls = tree.xpath("/html/body/div/main/article[1]/div/header/h2/a//@href")[0]
                reqs = requests.get(urls, headers=header_)
                trees = etree.HTML(reqs.content.decode("utf-8"))
                test = trees.xpath("/html/body/div/main/article/div/p")
                self.name = (tree.xpath("/html/body/div/main/article[1]/div/header/h2/a/text()")[0])
            else:
                test = tree.xpath("/html/body/div/main/article/div/p")
                self.name = (tree.xpath("/html/body/div/main/article/header/h1/text()")[0])
            for i in test:
                if not i.xpath("./text()"):
                    continue
                else:
                    try:
                        if i.xpath("./text()")[0] == '视频：':
                            self.url = (i.xpath('.//a[contains(@href, "https://pan")]/@href')[0])
                            self.key = (i.xpath("./text()")[1].strip().replace(r"\xa0 \xa0", ''))
                            break
                    except Exception as r:
                        self.url = ("已找到电影，但出现未知错误")
                        self.key = (r)
                        break
        except Exception as r:
            self.key = ("出问题了:" + str(r))


