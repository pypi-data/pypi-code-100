from glob import glob
from pathlib import Path

class PathHandler():

    @staticmethod
    def get_path(path: str = None) -> str:
        path = str(Path.cwd()) if path is None else path
        path[-1].replace('\\', '')
        return path

    @staticmethod
    def drop_last_folder_from_path(path: str):
        return "\\".join(path.split('\\')[:-1])

    @staticmethod
    def create_dir(path: str):
        Path(path).mkdir(mode=511, parents=True, exist_ok=True)

    def get_files(self, folder_path: str = None, file_type='json') -> list[str]:
        path = self.get_path(folder_path)
        return [f for f in glob(path + "\*." + file_type)]
