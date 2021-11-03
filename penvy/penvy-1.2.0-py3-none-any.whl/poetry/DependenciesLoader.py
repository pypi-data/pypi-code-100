from penvy.poetry import config_reader


class DependenciesLoader:
    def __init__(
        self,
        poetry_lock_path: str,
    ):
        self._poetry_lock_path = poetry_lock_path

    def load(self) -> dict:
        poetry_lock = config_reader.read(self._poetry_lock_path)
        dependencies = {}

        for package in poetry_lock["package"]:
            dependencies[package["name"]] = {
                "version": package["version"],
                "category": package["category"],
            }

        return dependencies

    def load_main(self) -> dict:
        dependencies = self.load()

        return {
            key: {
                "version": val["version"],
                "category": val["category"],
            }
            for key, val in dependencies.items()
            if val["category"] == "main"
        }

    def load_dev(self) -> dict:
        dependencies = self.load()

        return {
            key: {
                "version": val["version"],
                "category": val["category"],
            }
            for key, val in dependencies.items()
            if val["category"] == "dev"
        }
