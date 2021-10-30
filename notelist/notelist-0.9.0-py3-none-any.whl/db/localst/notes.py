"""Local Storage notes module."""

from typing import Optional

from notelist.db.base.notes import NoteManager


class LocalStNoteManager(NoteManager):
    """Local Storage note manager."""

    def __init__(self, root_dm: "LocalStorageManager"):
        """Initialize instance.

        :param root_dm: Root data manager.
        """
        self._root_dm = root_dm

    def _select_note(self, n: dict, tags: list[str], no_tags: bool) -> bool:
        """Return whether a note document should be included or not based on
        its tags.

        :param n: Note document.
        :param tags: If the note has any of these tags, the note is selected.
        :param no_tags: If the value is `True` and the note has no tags, the
        note is selected.
        :return: `True` if the note is selected or `False` otherwise.
        """
        k = "tags"
        note_tags = n[k] if k in n else []

        return (
            (len(note_tags) == 0 and no_tags) or
            any(map(lambda t: t in note_tags, tags)))

    def get_by_filter(
        self, notebook_id: str, archived: Optional[bool] = None,
        tags: Optional[list[str]] = None, no_tags: bool = False,
        last_mod: bool = False, asc: bool = True
    ) -> list[dict]:
        """Return all the note documents of a given notebook by a filter.

        :param notebook_id: Notebook ID.
        :param archived: State filter (include archived notes or not archived
        notes).
        :param tags: Tags filter (include notes that has any of these tags).
        This list contains tag names.
        :param no_tags: Notes with No Tags filter (include notes with no tags).
        This filter is only applicable if a tag filter has been provided, i.e.
        `tags` is not None).
        :param last_mod: `True` if notes should be sorted by their Last
        Modified timestamp. `False` if notes should be sorted by their Created
        timestamp (default).
        :param asc: Whether the notes order should be ascending (default) or
        not.
        :return: Note documents.
        """
        notes = self._root_dm.get_data()["notes"].items()

        # Filter by notebook
        notes = [
            {"id": _id} | n
            for _id, n in notes
            if n["notebook_id"] == notebook_id]

        # Filter by state
        if archived in (True, False):
            notes = [n for n in notes if n["archived"] == archived]

        # Order
        k = "last_modified" if last_mod else "created"
        notes = sorted(notes, key=lambda x: x[k], reverse=not asc)

        # Filter by tags and No Tags
        if tags is not None:
            notes = filter(
                lambda n: self._select_note(n, tags, no_tags), notes)
            notes = list(notes)

        return notes

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a note document given its ID.

        :param _id: Note ID.
        :return: Note document.
        """
        note = self._root_dm.get_data()["notes"].get(_id)

        if note is not None:
            note = {"id": _id} | note

        return note

    def put(self, note: dict):
        """Put a note document.

        If an existing document has the same ID as `note`, the existing
        document is replaced with `note`.

        :param notebook: Notebook document.
        """
        note = note.copy()
        _id = note.pop("id")

        data = self._root_dm.get_data()
        data["notes"][_id] = note

        self._root_dm.save_data(data)

    def delete(self, _id: str):
        """Delete a note document given its ID.

        :param _id: Note ID.
        """
        k = "notes"
        data = self._root_dm.get_data()

        if _id in data[k]:
            data[k].pop(_id)
            self._root_dm.save_data(data)
