from itertools import tee

def ngrams(sequence, n=2):
    """Return the ngrams generated from a sequence of items, as an iterator.

    Parameters
    ----------
    sequence : Sequence
        The source data to be converted into ngrams
    n : int, optional
        The degree of the ngrams, by default 2
    
    Notes
    -----
    Implementation based on nltk.util.ngrams
    https://github.com/nltk/nltk/blob/develop/nltk/util.py#L825
    """
    iterables = tee(sequence, n)
    for i, iterable in enumerate(iterables):
        for _ in range(i):
            next(iterable, None)
    return zip(*iterables)
