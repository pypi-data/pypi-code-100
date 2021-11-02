from io import (
    BytesIO,
    RawIOBase,
)
from pathlib import Path
from typing import Iterator, Tuple, List, cast, Union, IO, Any, BinaryIO, TextIO

from dataclasses import dataclass
from py4j.java_gateway import JavaObject, JavaGateway, JavaClass
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession

from .hdfsio import _HdfsBytesIo, _HdfsTextIo

HdfsPath = Union[str, JavaObject, Path]


class HdfsFs:
    """Provides access to an underlying HDFS filesystem"""

    def __init__(self, gateway: JavaGateway, java_fs: JavaObject):
        """Builds a new filesystem

        Args:
            gateway: The PY4J gateway used to communicate with the Java Virtual Machine that implements HDFS access
            java_fs: Handle to an `org.apache.hadoop.fs.FileSystem` object
        """
        self._gateway = gateway
        self._jfs = java_fs

    @classmethod
    def from_spark_session(cls, spark: SparkSession) -> "HdfsFs":
        """Builds a new filesystem from a Spark Session"""
        sc = spark.sparkContext
        gateway = sc._gateway  # type: ignore[attr-defined]
        jfs = gateway.jvm.org.apache.hadoop.fs.FileSystem
        return cls(gateway, jfs.get(sc._jsc.hadoopConfiguration()))  # type: ignore[attr-defined]

    def open(
        self,
        path: HdfsPath,
        mode: str = "rt",
        encoding: str = "UTF-8",
        permissions: int = 0o660,
    ) -> IO[Any]:
        """Opens the given path and returns a file like object

        The implementation is inspired by the standard open function and it should be possible to use this
        method as a drop in replacement for ordinary open invocations unless random access writes, which
        are not supported by HDFS, are used.

        Args:
            path: The path to open
            mode: A mode string similar to the one accepted by the standard open function. All flags except for `x` and `+` are implemented.
            encoding: The encoding to use, if working in text mode
            permissions: The permissions to apply, if the file is opened for writing
        """
        parsed_mode = _parse_mode(mode)

        # text mode
        if parsed_mode.t:
            jin, jout, _ = self._get_jin_out_streams(
                path,
                r=parsed_mode.r,
                w=parsed_mode.w,
                a=parsed_mode.a,
                overwrite=True,
                permissions=permissions,
            )
            try:
                jreader, jwriter = self._get_jreader_writer(
                    jin=jin, jout=jout, encoding=encoding
                )
                io = _HdfsTextIo(
                    self._gateway, java_reader=jreader, java_writer=jwriter
                )
                jin, jout = None, None

                # TODO:
                #  The code should be adapted to avoid this cast. Unfortunately
                #  this is not as simple as it seems, because there are some
                #  inconsistencies between TextIOBase and TextIO. Since most
                #  APIs that expect text file like objects expect TextIO,
                #  and the inconsistencies don't matter in 99% of all cases,
                #  it's better to have this cast here than in client code.
                return cast(TextIO, io)
            finally:
                if jin:
                    jin.close()
                if jout:
                    jout.close()
        # byte mode
        else:
            jin, jout, length = self._get_jin_out_streams(
                path,
                r=parsed_mode.r,
                w=parsed_mode.w,
                a=parsed_mode.a,
                overwrite=True,
                permissions=permissions,
            )

            bytes_io = _HdfsBytesIo(
                self._gateway, java_in=jin, java_out=jout, length=length
            )

            # TODO:
            #  The code should be adapted to avoid this cast. The same
            #  reasoning applies as for the cast a few lines above
            return cast(BinaryIO, bytes_io)

    def read_string(self, path: HdfsPath, *, encoding: str = "UTF-8") -> str:
        """Reads a file into a string

        Args:
            path: file path to read into a string
            encoding: optional, encoding of the string
        """
        jin = self._jfs.open(self._to_jfs_path(path))
        try:
            return self._j_io_utils.toString(jin, encoding)
        finally:
            jin.close()

    def write_string(
        self,
        path: HdfsPath,
        data: str,
        *,
        encoding: str = "UTF-8",
        overwrite: bool = False,
        permissions: int = 0o660,
    ) -> None:
        """Writes a string into a file

        Args:
            path: file path to write data into
            data: data to write
            encoding: optional, encoding of the data
            overwrite: if True overwrite existing file, otherwise raise an exception
            permissions: set file permission for the created file
        """
        jout = self._jfs.create(self._to_jfs_path(path), overwrite)
        try:
            self.set_permissions(path, permissions)
            self._j_io_utils.write(data, jout, encoding)
        finally:
            jout.close()

    def read_bytes(self, path: HdfsPath) -> bytes:
        """Reads a file into a byte array"""

        # The implementation of this method has been adapted
        # to be considerably more memory efficient, at the
        # expense of simplicity. Consult the implementation
        # of _HdfsBytesIo.readinto for a more detailed
        # discussion.
        buf_size = 1024 * 8
        buffer = bytearray(buf_size)

        bytes_io = BytesIO()
        with cast(RawIOBase, self.open(path, mode="rb")) as f:
            while True:
                read = f.readinto(buffer)
                if read:
                    bytes_io.write(buffer[0:read])
                    if read < buf_size:
                        break
                else:
                    break

        return bytes_io.getvalue()

    def write_bytes(
        self,
        path: HdfsPath,
        data: bytes,
        *,
        overwrite: bool = False,
        permissions: int = 0o660,
    ) -> None:
        """Writes a byte array into a file

        Args:
            path: file path to write data into
            data: data to write
            overwrite: if True overwrite existing file, otherwise raise an exception
            permissions: set file permission for the created file
        """
        jout = self._jfs.create(self._to_jfs_path(path), overwrite)
        try:
            self.set_permissions(path, permissions)
            jout.write(data)
        finally:
            jout.close()

    def mkdirs(self, path: HdfsPath, *, permissions: int = 0o770) -> bool:
        """Creates the given directory, creating parent directories as needed

        Args:
            path: path to create
            permissions: directory permissions for the created path
        """
        jperms = self._mode_bits_to_fs_permission(permissions)
        jpath = self._to_jfs_path(path)
        return self._jfs.mkdirs(jpath, jperms)

    def set_permissions(self, path: HdfsPath, permissions: int) -> None:
        """Sets the given permissions

        Args:
            path: path to change permissions
            permissions: permissions for the path
        """
        jperms = self._mode_bits_to_fs_permission(permissions)
        jpath = self._to_jfs_path(path)
        self._jfs.setPermission(jpath, jperms)

    def get_permissions(self, path: HdfsPath) -> int:
        """Returns the permission bits for the given path"""
        return self._get_file_status(path).getPermission().toShort()

    def walk(self, path: HdfsPath) -> Iterator[Tuple[str, List[str], List[str]]]:
        """Behaves similar to os.walk"""
        if not self._get_file_status(path).isDirectory():
            yield from ()
        else:
            jpath = self._to_jfs_path(path)

            try:
                stati = self._jfs.listStatus(jpath)

                dirs = []
                file_names = []

                for status in stati:
                    if status.isDirectory():
                        dirs.append(status.getPath())
                    elif status.isFile():
                        file_names.append(status.getPath().getName())

                dir_names = [d.getName() for d in dirs]
                stripped_path = self._strip_scheme_and_auth(jpath)
                yield stripped_path, dir_names, file_names

                for d in dirs:
                    yield from self.walk(d)

            except Py4JJavaError as e:
                if "permission denied" in e.java_exception.getMessage().lower():
                    yield from ()

    def delete(self, path: HdfsPath, *, recursive: bool = False) -> bool:
        """Deletes a single file or directory

        Args:
            path: path to be deleted
            recursive: if True will delete child elements, otherwise will abort if child elements exist
        """
        jpath = self._to_jfs_path(path)
        return self._jfs.delete(jpath, recursive)

    def listdir(self, path: HdfsPath) -> List[str]:
        """Lists the contents of the directory"""
        jpath = self._to_jfs_path(path)
        stati = self._jfs.listStatus(jpath)
        return [s.getPath().getName() for s in stati]

    def close(self) -> None:
        self._jfs.close()

    def exists(self, path: HdfsPath) -> bool:
        """Tests if the given path exists"""
        return self._jfs.exists(self._to_jfs_path(path))

    def rename(self, src: HdfsPath, dst: HdfsPath) -> bool:
        """Renames the given file or directory

        See https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/fs/FileSystem.html#rename-org.apache.hadoop.fs.Path-org.apache.hadoop.fs.Path-
        for the underlying Java method.

        Returns:
            True if successful
        """
        return self._jfs.rename(self._to_jfs_path(src), self._to_jfs_path(dst))

    def _get_file_status(self, path: HdfsPath) -> JavaObject:
        """See https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/fs/FileSystem.html#getFileStatus-org.apache.hadoop.fs.Path-"""
        jpath = self._to_jfs_path(path)
        return self._jfs.getFileStatus(jpath)

    def _mode_bits_to_fs_permission(self, mode: int) -> JavaObject:
        fs_permission = self._gateway.jvm.org.apache.hadoop.fs.permission.FsPermission
        return fs_permission(mode)

    def _get_jreader_writer(
        self, *, jin: JavaObject, jout: JavaObject, encoding: str
    ) -> JavaObject:
        """Obtains readers and writers based on the given input and output streams

        Args:
            jin: A https://docs.oracle.com/javase/8/docs/api/java/io/InputStream.html
            jout: A https://docs.oracle.com/javase/8/docs/api/java/io/OutputStream.html
            encoding: https://docs.oracle.com/javase/8/docs/api/java/io/Reader.html and a https://docs.oracle.com/javase/8/docs/api/java/io/Writer.html

        Returns:
            https://docs.oracle.com/javase/8/docs/api/java/io/Reader.html and a https://docs.oracle.com/javase/8/docs/api/java/io/Writer.html
        """
        jreader = None
        jwriter = None

        if jin:
            jreader0 = self._j_input_stream_reader(jin, encoding)
            jreader = self._j_buffered_reader(jreader0)

        if jout:
            jwriter0 = self._j_output_stream_writer(jout, encoding)
            jwriter = self._j_buffered_writer(jwriter0)

        return jreader, jwriter

    def _get_jin_out_streams(
        self,
        path: HdfsPath,
        *,
        r: bool,
        w: bool,
        a: bool,
        overwrite: bool,
        permissions: int,
    ) -> Tuple[JavaObject, JavaGateway, int]:
        """Obtains input and output streams for the given path

        Args:
            path: The path to read/write
            r: Open for reading?
            w: Open for writing?
            a: Open for appending?
            overwrite: Overwrite existing files on creation?
            permissions: Permission bits

        Returns:
         Java input (see https://docs.oracle.com/javase/8/docs/api/java/io/InputStream.html), output (see https://docs.oracle.com/javase/8/docs/api/java/io/OutputStream.html) streams and the file length.
        """
        jpath = self._to_jfs_path(path)

        def get_jin() -> JavaObject:
            return self._jfs.open(jpath) if r else None

        def get_length() -> int:
            return self._jfs.getFileStatus(jpath).getLen() if r else 0

        def get_jout() -> JavaObject:
            jperms = self._mode_bits_to_fs_permission(permissions)

            jout = None
            if a:
                jout = self._jfs.append(jpath)
            elif w:
                jout = self._jfs.create(jpath, overwrite)

            if jout:
                self._jfs.setPermission(jpath, jperms)
            return jout

        jin = get_jin()
        try:
            length = get_length()
            jout = get_jout()
            tmp_in = jin
            jin = None
            return (tmp_in, jout, length)
        finally:
            if jin:
                jin.close()

    def _to_jfs_path(self, path: HdfsPath) -> JavaObject:
        """Converts to an org.apache.hadoop.fs.Path"""
        clazz = self._gateway.jvm.org.apache.hadoop.fs.Path
        return clazz(str(path))

    @property
    def _j_io_utils(self) -> JavaClass:
        return self._gateway.jvm.org.apache.commons.io.IOUtils

    @property
    def _j_input_stream_reader(self) -> JavaClass:
        return self._gateway.jvm.java.io.InputStreamReader

    @property
    def _j_buffered_reader(self) -> JavaClass:
        return self._gateway.jvm.java.io.BufferedReader

    @property
    def _j_output_stream_writer(self) -> JavaClass:
        return self._gateway.jvm.java.io.OutputStreamWriter

    @property
    def _j_buffered_writer(self) -> JavaClass:
        return self._gateway.jvm.java.io.BufferedWriter

    def _strip_scheme_and_auth(self, path: str) -> str:
        """See https://hadoop.apache.org/docs/r3.0.3/api/org/apache/hadoop/fs/Path.html#getPathWithoutSchemeAndAuthority-org.apache.hadoop.fs.Path-"""
        clazz = self._gateway.jvm.org.apache.hadoop.fs.Path
        return str(clazz.getPathWithoutSchemeAndAuthority(path))


@dataclass(frozen=True)
class _ParsedMode:
    r: bool
    a: bool
    w: bool
    b: bool

    @property
    def t(self) -> bool:
        return not self.b


def _parse_mode(mode: str) -> _ParsedMode:
    def raise_invalid_mode():
        raise ValueError(f"invalid mode: '{mode}'")

    dupes = len(set(mode)) < len(mode)
    if dupes:
        raise_invalid_mode()

    illegal_chars = set(mode).difference(set("rwatb"))
    if illegal_chars:
        raise_invalid_mode()

    if "b" in mode and "t" in mode:
        raise ValueError("can't have text and binary mode at once")

    arws = sum(1 for c in mode if c in "arw")
    if arws > 1:
        raise ValueError("must have exactly one of read/write/append mode")

    b = "b" in mode
    a = "a" in mode
    r = "r" in mode
    w = "w" in mode
    return _ParsedMode(r=r, a=a, w=w, b=b)
