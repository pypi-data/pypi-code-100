from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from pysparkbundle.write.PathWriterDecorator import PathWriterDecorator


@DecoratedDecorator
class delta_write_errorifexists(PathWriterDecorator):  # noqa: N801
    _mode = "errorifexists"
    _writer_service = "pysparkbundle.delta.writer"
