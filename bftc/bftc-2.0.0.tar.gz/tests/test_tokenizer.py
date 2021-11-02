from bftc import tokenizer, tokens


def test_plus_tokenization():
    token = tokenizer.tokenize("+")

    assert isinstance(token, tokens.IncrementCellValueToken)


def test_minus_tokenization():
    token = tokenizer.tokenize("-")

    assert isinstance(token, tokens.DecrementCellValueToken)


def test_dot_tokenization():
    token = tokenizer.tokenize(".")

    assert isinstance(token, tokens.PutCellValueToken)


def test_comma_tokenization():
    token = tokenizer.tokenize(",")

    assert isinstance(token, tokens.GetCellValueToken)


def test_more_sign_tokenization():
    token = tokenizer.tokenize(">")

    assert isinstance(token, tokens.NextCellToken)


def test_less_sign_tokenization():
    token = tokenizer.tokenize("<")

    assert isinstance(token, tokens.PreviousCellToken)


def test_open_square_bracket_tokenization():
    token = tokenizer.tokenize("[")

    assert isinstance(token, tokens.LoopStartToken)


def test_close_square_bracket_tokenization():
    token = tokenizer.tokenize("]")

    assert isinstance(token, tokens.LoopEndToken)


def test_invalid_syntax_tokenization():
    token = tokenizer.tokenize("@")

    assert isinstance(token, tokens.InvalidSyntaxToken)
