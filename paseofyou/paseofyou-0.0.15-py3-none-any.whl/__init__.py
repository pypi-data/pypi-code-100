from paseofyou import movie


def name(strs: str):
    video = movie.movie(strs.strip())
    print(video.name, video.url, video.key)
    return (video.name, video.url, video.key)
