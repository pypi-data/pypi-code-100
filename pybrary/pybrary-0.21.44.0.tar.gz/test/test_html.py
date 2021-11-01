from pybrary.html import Parser


def test_n_parser():
    url = "https://pypi.org/search?q=pybrary"
    root = Parser().get(url)
    name = version = None
    for pkg in (n for n in root if 'package-snippet' in n.classes):
        for node in (n for n in pkg if 'package-snippet__name' in n.classes):
            if node.text=='pybrary':
                name = node.text
                # print(f'{name = }')
                for ver in (n for n in pkg if 'package-snippet__version' in n.classes):
                    version = ver.text
                    # print(f'{version = }')

    assert name=='pypbrary'
    assert version


if __name__=='__main__': test_n_parser()
