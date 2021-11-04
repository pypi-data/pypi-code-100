from intentBox.segmentation.simple import Segmenter
from quebra_frases import chunk, get_common_chunks

try:
    import RAKEkeywords
except ImportError:
    RAKEkeywords = None


def rake(text, lang="en-us"):
    if not RAKEkeywords:
        raise ImportError("failed to import module RAKEkeywords")
    return RAKEkeywords.Rake(lang=lang).extract_keywords(text)


def segment_keywords(text, lang="en-us", simple=False):
    if RAKEkeywords and lang and not simple:
        return chunk(text, delimiters=[_[0] for _ in rake(text, lang)])
    return text.split(" ")

