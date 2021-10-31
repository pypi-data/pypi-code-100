"""Base notes module."""

from typing import Optional


class NoteManager:
    """Note manager.

    This is an abstract class and should not be instantiated.
    """

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
        raise NotImplementedError()

    def get_by_id(_id: str) -> Optional[dict]:
        """Return a note document given its ID.

        :param _id: Note ID.
        :return: Note document.
        """
        raise NotImplementedError()

    def put(self, note: dict):
        """Put a note document.

        If an existing document has the same ID as `note`, the existing
        document is replaced with `note`.

        :param note: Note document.
        """
        raise NotImplementedError()

    def delete(self, _id: str):
        """Delete a note document given its ID.

        :param _id: Note ID.
        """
        raise NotImplementedError()
