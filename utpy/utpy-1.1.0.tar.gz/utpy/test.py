

import utpy

url = 'https://www.youtube.com/watch?v=3Q_8lPkJm2M' # video or playlist url
yt = utpy.Load(url)

# return all information as dic
# print(yt.data)

# download video or videos of playlist
yt.download()