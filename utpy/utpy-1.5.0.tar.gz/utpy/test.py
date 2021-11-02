import utpy
import urllib3
from dicts import replace_dict
import re
import json

url = 'https://www.youtube.com/playlist?list=PLSccONlqbvweNK-dhNDSevhmR9ngTyTSv' # video or playlist url
yt = utpy.Load(url)
# open('utpy-data.txt', 'w', encoding='utf-8').write(str(yt.data))
yt.download()



# url = https://www.youtube.com/watch?v=Zyhb6SMx1B0&list=PLSccONlqbvweEiAvuU0ELKNs1atxxaRZ4&index=46
# PS E:\programming\utpy> & "C:/Program Files/Python39/python.exe" e:/programming/utpy/utpy/test.py
# Traceback (most recent call last):
#   File "e:\programming\utpy\utpy\test.py", line 10, in <module>
#     yt.download()
#   File "e:\programming\utpy\utpy\utpy.py", line 189, in download
#     save_to = self._get_dl_dir
#   File "e:\programming\utpy\utpy\utpy.py", line 174, in _get_dl_dir
#     pl_title = self.data['playlist']['title']
# TypeError: 'NoneType' object is not subscriptable







# http = urllib3.PoolManager()
# url = 'https://www.youtube.com/playlist?list=PLSccONlqbvweEiAvuU0ELKNs1atxxaRZ4'
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.76 Safari/537.36",
#     "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,ar;q=0.6"
#     }
# response = http.request('GET', url, headers=headers)

# pl_html = response.data.decode('utf-8')

# for k in replace_dict:
#     pl_html = pl_html.replace(k, replace_dict[k])
# videos_data = re.findall(r'(\[{\"playlistVideoRenderer\":.*}]}}}]}}])', pl_html)[0]
# data = json.loads(videos_data)
# # for i in data:
# #     print(i['playlistVideoRenderer']['commandMetadata'])
# print(data[0]['playlistVideoRenderer']['lengthSeconds'])
# # print(type(data))
# # open('videos_data_1.txt', 'w', encoding="utf-8").write(str(data[0]))