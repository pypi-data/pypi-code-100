import pathlib


class FilePath:
    def __init__(self, config, root, date, name):
        if not isinstance(root, pathlib.Path):
            root = pathlib.Path(root).resolve()

        if not root.is_dir():
            raise ValueError("root is not a directory")
        self.bells_root = config.root
        self.root = root.resolve()
        self.date = str(date)
        self.name = str(name) + "-0000"

        count = 0
        while self.path.exists():
            self.name = f"{name}-{count:04}"
            count += 1

    @property
    def path(self):
        "Path as a pathlib.Path"
        return self.root / f"{self.date}-{self.name}.wav"

    @property
    def spath(self):
        "Path as a string"
        return str(self.path)

    @property
    def linked_path(self):
        "Returns the path at which this file will be linked to"
        split = self.root.relative_to(self.bells_root / "structural").parts
        dir_ = self.bells_root / "chronological" / self.date.replace("-", "/")
        dir_.mkdir(parents=True, exist_ok=True)
        return dir_ / ("--".join(split) + "--" + self.name + ".wav")

    def link(self):
        depth = self.linked_path.relative_to(self.bells_root)
        path = self.path.relative_to(self.bells_root)
        for _ in depth.parts[:-1]:
            path = ".." / path
        self.linked_path.symlink_to(path)
