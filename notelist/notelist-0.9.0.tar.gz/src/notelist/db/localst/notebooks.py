"""Local Storage notebooks module."""

from typing import Optional

from notelist.db.base.notebooks import NotebookManager


class LocalStNotebookManager(NotebookManager):
    """Local Storage notebook manager."""

    def __init__(self, root_dm: "LocalStorageManager"):
        """Initialize instance.

        :param root_dm: Root data manager.
        """
        self._root_dm = root_dm

    def get_by_user(self, user_id: str) -> list[dict]:
        """Return all the notebook documents of a given user.

        :param user_id: User ID.
        """
        nbs = self._root_dm.get_data()["notebooks"].items()
        nbs = [{"id": _id} | n for _id, n in nbs if n["user_id"] == user_id]

        return sorted(nbs, key=lambda n: n["name"])

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a notebook document given its ID.

        :param _id: Notebook ID.
        :return: Notebook document if it exists or None otherwise.
        """
        notebook = self._root_dm.get_data()["notebooks"].get(_id)

        if notebook is not None:
            notebook = {"id": _id} | notebook

        return notebook

    def get_by_name(self, user_id: str, name: str) -> Optional[dict]:
        """Return a notebook document given its user and name.

        :param user_id: Notebook user ID.
        :param name: Notebook name.
        :return: Notebook document if it exists or None otherwise.
        """
        notebook = None

        for _id, n in self._root_dm.get_data()["notebooks"].items():
            if n["user_id"] == user_id and n["name"] == name:
                notebook = {"id": _id} | n
                break

        return notebook

    def put(self, notebook: dict):
        """Put a notebook document.

        If an existing document has the same ID as `notebook`, the existing
        document is replaced with `notebook`.

        :param notebook: Notebook document.
        """
        notebook = notebook.copy()
        _id = notebook.pop("id")

        data = self._root_dm.get_data()
        data["notebooks"][_id] = notebook

        self._root_dm.save_data(data)

    def delete(self, _id: str):
        """Delete a notebook document given its ID.

        :param _id: Notebook ID.
        """
        k = "notebooks"
        data = self._root_dm.get_data()

        if _id in data[k]:
            data[k].pop(_id)
            self._root_dm.save_data(data)
