from lotide_luna import __version__


def get_version(request):
    return {
        'LUNA_VERSION': __version__
    }
