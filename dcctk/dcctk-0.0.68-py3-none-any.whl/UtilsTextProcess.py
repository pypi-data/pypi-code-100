def read_text_as_sentences(fp):
    """Read text file as a sequency of sentences

    Parameters
    ----------
    fp : str
        Path to UTF-8 encoded plain text file.

    Yields
    -------
    str
        A string representing a sentence. A sentence
        corresponds to a line in the file.
    """
    with open(fp, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "": continue
            yield line
