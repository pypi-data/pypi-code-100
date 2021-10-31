

import utpy

url = 'https://www.youtube.com/playlist?list=PLSccONlqbvweEiAvuU0ELKNs1atxxaRZ4' # video or playlist url
yt = utpy.Load(url)

# return all information as dic
# print(yt.data)

# download video or videos of playlist
yt.download()