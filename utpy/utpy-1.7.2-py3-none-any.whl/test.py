import utpy

url = 'https://www.youtube.com/playlist?list=PLSccONlqbvweNK-dhNDSevhmR9ngTyTSv'
y = utpy.Load(url)

y.download()