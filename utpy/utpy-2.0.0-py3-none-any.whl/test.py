import utpy

# url = 'https://www.youtube.com/playlist?list=PLSccONlqbvweNK-dhNDSevhmR9ngTyTSv'
url = 'https://www.youtube.com/playlist?list=PL56IcDjrf3YJr__TEOJ2UOv3jCzht1_yc'

y = utpy.Load(url)
y.download
