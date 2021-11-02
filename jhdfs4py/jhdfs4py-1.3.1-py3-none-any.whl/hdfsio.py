from io import RawIOBase, SEEK_SET, SEEK_CUR, TextIOBase

from py4j.java_gateway import JavaGateway, JavaObject, JavaClass


class _HdfsBytesIo(RawIOBase):
    """IO class that wraps Java input and output streams"""

    def __init__(
        self,
        gateway: JavaGateway,
        *,
        java_in: JavaObject,
        java_out: JavaObject,
        length: int,
    ):
        """Initialize IO instance

        Args:
            gateway: See https://www.py4j.org/py4j_java_gateway.html#py4j.java_gateway.JavaGateway
            java_in: See https://docs.oracle.com/javase/8/docs/api/java/io/InputStream.html
            java_out: https://docs.oracle.com/javase/8/docs/api/java/io/OutputStream.html
            length: The length of the underlying file (only relevant when reading)
        """
        self._gateway = gateway
        self._java_in = java_in
        self._java_out = java_out
        self._length = length

    def close(self):
        if self._java_in:
            self._java_in.close()
        if self._java_out:
            self._java_out.close()

        super().close()

    def readall(self):
        return self._j_io_utils.toByteArray(self._java_in)

    def readinto(self, buf):
        # Unfortunately, transferring large amounts of data from Java to Python can
        # easily exhaust available memory, even for moderate amounts of data,
        # if not done carefully.
        #
        # The original implementation of this method just wrote the maximum
        # amount of data into a Java byte array, and transferred that to `buf`.
        # However, since byte arrays are transferred from Java to Python by
        # value (see https://www.py4j.org/advanced_topics.html#byte-array-byte)
        # this approach consumes large amounts of excess memory even in the
        # best case. Assuming that buf has B bytes, we would have
        #   1) B bytes for the array on the Java side
        #   2) B bytes for the array that is passed by value to Python
        #   3) B bytes for buf itself
        #
        # To circumvent this problem, this method has been adapted to fill
        # buff kilobyte by kilobyte. This conserves huge amounts of memory
        # for large arrays, but makes the implementation a bit more involved.
        step_size = 1024 * 1024
        copied_total = 0

        bout = self._j_byte_array_output_stream(min(step_size, len(buf)))
        while True:
            last_step = copied_total + step_size >= len(buf)
            step_bytes = len(buf) - copied_total if last_step else step_size
            copied = self._j_io_utils.copyLarge(self._java_in, bout, 0, step_bytes)
            if copied > 0:
                buf[copied_total : copied_total + copied] = bout.toByteArray()
                copied_total += copied
                bout.reset()
            else:
                break

            if last_step:
                break

        return copied_total if copied_total > 0 else None

    def seek(self, offset, whence=SEEK_SET):
        if whence == SEEK_SET:
            self._java_in.seek(offset)
        elif whence == SEEK_CUR:
            self._java_in.seek(offset + self._java_in.getPos())
        else:
            self._java_in.seek(offset + self._length)

        return self._java_in.getPos()

    def tell(self):
        return self._java_in.getPos()

    def seekable(self):
        return bool(self._java_in)

    def writable(self):
        return bool(self._java_out)

    def readable(self):
        return bool(self._java_in)

    def write(self, b):
        self._java_out.write(b)
        return len(b)

    @property
    def _j_io_utils(self) -> JavaClass:
        """See https://commons.apache.org/proper/commons-io/javadocs/api-2.6/org/apache/commons/io/IOUtils.html"""
        return self._gateway.jvm.org.apache.commons.io.IOUtils

    @property
    def _j_byte_array_output_stream(self) -> JavaClass:
        """See https://docs.oracle.com/javase/8/docs/api/?java/io/ByteArrayOutputStream.html"""
        return self._gateway.jvm.java.io.ByteArrayOutputStream


class _HdfsTextIo(TextIOBase):
    """IO class that wraps Java readers and output writers"""

    def __init__(
        self, gateway: JavaGateway, *, java_reader: JavaObject, java_writer: JavaObject
    ):
        """Initialize IO instance

        Args:
            gateway: See https://www.py4j.org/py4j_java_gateway.html#py4j.java_gateway.JavaGateway
            java_reader: See https://docs.oracle.com/javase/8/docs/api/java/io/Reader.html
            java_writer: See https://docs.oracle.com/javase/8/docs/api/java/io/Writer.html
        """
        self._gateway = gateway
        self._java_reader = java_reader
        self._java_writer = java_writer

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()

        if not line:
            raise StopIteration
        return line

    def read(self, size=-1):
        if size < 0:
            return self._j_io_utils.toString(self._java_reader)
        else:
            string_writer = self._j_string_writer()
            self._j_io_utils.copyLarge(self._java_reader, string_writer, 0, size)
            return string_writer.toString()

    def readline(self):
        return self._java_reader.readLine()

    def close(self):
        if self._java_reader:
            self._java_reader.close()
        if self._java_writer:
            self._java_writer.close()

        self._java_reader = None
        self._java_writer = None

        super().close()

    def write(self, s):
        self._java_writer.write(s)
        return len(s)

    def writable(self):
        return bool(self._java_writer)

    def readable(self):
        return bool(self._java_reader)

    @property
    def _j_io_utils(self) -> JavaClass:
        """See https://commons.apache.org/proper/commons-io/javadocs/api-2.6/org/apache/commons/io/IOUtils.html"""
        return self._gateway.jvm.org.apache.commons.io.IOUtils

    @property
    def _j_string_writer(self) -> JavaClass:
        """See https://docs.oracle.com/javase/8/docs/api/java/io/StringWriter.html"""
        return self._gateway.jvm.java.io.StringWriter
