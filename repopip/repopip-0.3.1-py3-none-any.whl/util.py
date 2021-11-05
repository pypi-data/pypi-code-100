from flask import url_for
from hurry.filesize import size, alternative


def filesize(bytes_int: int):
    return size(bytes_int, system=alternative)


def url( url : dict ):
    if( 'lang' in url.keys()):
        return url_for(url['path'], lang=url['lang'])
    else:
        return url_for(url['path'])