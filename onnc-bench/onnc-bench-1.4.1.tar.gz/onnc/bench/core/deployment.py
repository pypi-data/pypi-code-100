from typing import List, Dict, Union
from pathlib import Path
import shutil
import json
import os


class Deployment:
    """
    Deployment is a container class for built artifacts and reports
    """
    META_FNAME = Path('.deployment.json')

    def __init__(self, path: Union[None, Path]):
        if path:
            self.base_path = Path(path)

            # if self.base_path.joinpath(self.META_FNAME).exists():
            #     self.load()
            # else:
            self.compiled_files = [
                x for x in os.listdir(self.base_path / 'src')]
            self.report_path = self.base_path / 'report.json'
            self.report = dict(json.loads(open(self.report_path, 'r').read()
                                          )["metrics"])
            self.compile_logs = json.loads(open(self.report_path, 'r').read()
                                           )["logs"]

            # self.save()

    def __str__(self):
        return json.dumps(self.meta, sort_keys=True, indent=2)

    def __repr__(self):
        return self.meta

    @property
    def meta(self):
        return {"base_path": str(self.base_path),
                "compiled_files": [str(x) for x in self.compiled_files],
                "report_path": str(self.report_path),
                "report": self.report
                }

    def save(self):
        _path = self.base_path / self.META_FNAME
        open(_path, 'w').write(json.dumps(self.meta, sort_keys=True, indent=4))

    def load(self):
        meta = json.loads(open(self.base_path / self.META_FNAME, 'r').read())

        self.base_path = meta["base_path"]
        self.compiled_files = meta["compiled_files"]
        self.report_path = meta["report_path"]
        self.report = json.loads(open(meta["report_path"], "r").read())

    def load_raw(self):
        """Scan folder and construct the object"""
        pass

    def deploy(self, target: Path):
        """Copy the deployment folder to target

        Copy the deployment folder to target and reconstruct the meta

        """
        os.remove(self.base_path / self.META_FNAME)
        shutil.copytree(self.base_path, target)
        deployment = Deployment(target)
        return deployment
