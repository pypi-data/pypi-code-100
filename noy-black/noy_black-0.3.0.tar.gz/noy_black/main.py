from concurrent.futures import ProcessPoolExecutor
from blib2to3.pgen2.parse import Parser, token
from blib2to3.pgen2 import driver
from unittest import mock
import pkg_resources
import encodings
import codecs
import re

registered = False

grammar_file = pkg_resources.resource_filename("noy_black", "Grammar.txt")

original_load_packaged_grammar = driver.load_packaged_grammar
original_generate_pickle_name = driver._generate_pickle_name


def _generate_pickle_name(gt, cache_dir=None):
    result = original_generate_pickle_name(gt, cache_dir=cache_dir)
    if result:
        return result.replace(".pickle", ".noy.pickle")
    return result


def load_packaged_grammar(package, grammar_source, cache_dir=None):
    return original_load_packaged_grammar(package, grammar_file, cache_dir=cache_dir)


def spec_search_function(s):
    if s != "spec":
        return None
    utf8 = encodings.search_function("utf8")

    return codecs.CodecInfo(
        name="spec",
        encode=utf8.encode,
        decode=utf8.decode,
        streamreader=encodings.utf_8.StreamReader,
        streamwriter=encodings.utf_8.StreamWriter,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
    )


def register():
    global registered
    if registered:
        return

    registered = True

    mock.patch.multiple(
        driver,
        load_packaged_grammar=load_packaged_grammar,
        _generate_pickle_name=_generate_pickle_name,
    ).start()

    import black

    codecs.register(spec_search_function)

    def visit_setup_teardown_stmts(self, node):
        yield from self.line()
        yield from self.visit_default(node)

    black.LineGenerator.visit_setup_teardown_stmts = visit_setup_teardown_stmts

    def visit_describe_stmt(self, node):
        yield from self.line()
        yield from self.visit_default(node)

    black.LineGenerator.visit_describe_stmt = visit_describe_stmt

    def visit_it_stmt(self, node):
        yield from self.line()
        yield from self.visit_default(node)

    black.LineGenerator.visit_it_stmt = visit_it_stmt

    original_assert_equivalent = black.assert_equivalent

    def assert_equivalent(src, dst):
        if src and re.match(r"#\s*coding\s*:\s*spec", src.split("\n")[0]):
            m = __import__("noseOfYeti.tokeniser.spec_codec")
            spec_codec = m.tokeniser.spec_codec.codec()
            spec_codec.register()
            src = spec_codec.translate(src)
            dst = spec_codec.translate(dst)
        original_assert_equivalent(src, dst)

    original_classify = Parser.classify

    def classify(self, type, value, context):
        special = [
            "it",
            "ignore",
            "context",
            "describe",
            "before_each",
            "after_each",
        ]
        if type == token.NAME and value in special:
            dfa, state, node = self.stack[-1]
            if node and node[-1]:
                if node[-1][-1].type < 256 and node[-1][-1].type not in (
                    token.INDENT,
                    token.DEDENT,
                    token.NEWLINE,
                    token.ASYNC,
                ):
                    return self.grammar.tokens.get(token.NAME)
        return original_classify(self, type, value, context)

    mock.patch.object(black, "assert_equivalent", assert_equivalent).start()
    mock.patch.object(Parser, "classify", classify).start()


class CustomProcessPoolExecutor(ProcessPoolExecutor):
    def __init__(self, *args, **kwargs):
        kwargs["initializer"] = register
        super().__init__(*args, **kwargs)


def main():
    register()

    import black

    mock.patch.object(black, "ProcessPoolExecutor", CustomProcessPoolExecutor).start()
    black.patched_main()
