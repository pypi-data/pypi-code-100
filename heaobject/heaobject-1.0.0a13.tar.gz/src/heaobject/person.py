
from .root import  AbstractDesktopObject
from typing import Optional, List


class Person(AbstractDesktopObject):
    """
    Represents a Person
    """
    def __init__(self):
        super().__init__()
        # id is a super field
        #name is inherited in super
        self.__title: Optional[str] = None
        self.__email: Optional[str] = None

    @property
    def email(self) -> str:
        """
          The person's email (Optional) .
        """
        return self.__email

    @email.setter
    def email(self, email: Optional[str]) -> None:
        self.__email = str(email) if email is not None else None

    @property
    def title(self) -> str:
        """
          The Person's title (Optional).
        """
        return self.__title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self.__title = str(title) if title is not None else None

