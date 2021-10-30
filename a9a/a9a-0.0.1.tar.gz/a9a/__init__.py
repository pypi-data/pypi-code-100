import a9a.encoder
import a9a.decoder
import a9a.dir_reader
import a9a.dir_writer


class Archive:
    def __init__(self, nodes=None):
        if nodes is None:
            nodes = {}
        self.content = nodes

    def to_bytes(self):
        return b"a9a\n" + encoder.encode_nodes(self.content)

    def __repr__(self):
        return f"Archive({self.content})"

    @staticmethod
    def from_bytes(bts):
        assert bts[:4] == b"a9a\n"
        return Archive(decoder.decode_nodes(bts[4:])[0])

    def to_directory(self, dir_path):
        return dir_writer.write_directory(dir_path, self.content)

    @staticmethod
    def from_directory(dir_path):
        return Archive(dir_reader.read_directory(dir_path)[1])
