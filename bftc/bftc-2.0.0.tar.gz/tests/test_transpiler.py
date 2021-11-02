from bftc import transpiler, tokens


def test_next_cell_token_transpilation():
    code = transpiler.transpile(tokens.NextCellToken())

    assert code == "i++;"


def test_previous_cell_token_transpilation():
    code = transpiler.transpile(tokens.PreviousCellToken())

    assert code == "i--;"


def test_increment_cell_token_transpilation():
    code = transpiler.transpile(tokens.IncrementCellValueToken())

    assert code == "arr[i]++;"


def test_decrement_cell_token_transpilation():
    code = transpiler.transpile(tokens.DecrementCellValueToken())

    assert code == "arr[i]--;"


def test_loop_start_token_transpilation():
    code = transpiler.transpile(tokens.LoopStartToken())

    assert code == "while(arr[i]) {"


def test_loop_end_token_transpilation():
    code = transpiler.transpile(tokens.LoopEndToken())

    assert code == "}"


def test_get_cell_value_token_transpilation():
    code = transpiler.transpile(tokens.GetCellValueToken())

    assert code == "arr[i] = getchar();"


def test_put_cell_value_token_transpilation():
    code = transpiler.transpile(tokens.PutCellValueToken())

    assert code == "putchar(arr[i]);"
