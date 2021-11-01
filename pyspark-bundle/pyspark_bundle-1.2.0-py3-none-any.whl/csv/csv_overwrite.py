from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from pysparkbundle.write.PathWriterDecorator import PathWriterDecorator


@DecoratedDecorator
class csv_overwrite(PathWriterDecorator):  # noqa: N801
    _mode = "overwrite"
    _writer_service = "pysparkbundle.csv.writer"
