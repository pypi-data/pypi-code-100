from paseofyou import movie


def name(strs: str):
    movie.movie(strs.strip())
    print(movie.name, movie.url, movie.key)
    return (movie.name, movie.url, movie.key)
