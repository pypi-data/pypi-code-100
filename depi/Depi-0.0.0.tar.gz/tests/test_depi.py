import builtins

from depi import hello_world

def test_hello_world(monkeypatch):
    # Given

    # When
    print_input = ''
    def mock_print(str_):
        nonlocal print_input
        print_input = str_
    with monkeypatch.context() as ctx:
        ctx.setattr(builtins, 'print', mock_print)
        hello_world()

    # Then
    assert print_input == 'hello_world'
