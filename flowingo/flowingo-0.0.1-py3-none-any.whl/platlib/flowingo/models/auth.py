import datetime
from typing import Any, Optional, NoReturn
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from flowingo.models.base import Base

# # RBAC model of permissions
# class Role(Base):
#     __tablename__ = "roles"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String, unique=True)
#
#     # relations
#     users = relationship("User", uselist=True, back_populates="role")
#
#     def __repr__(self) -> str:
#         return f'<Role {self.id}: level {self.level} title {self.title}>'


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    # role = Column(Integer, ForeignKey('role.id'))
    username = Column(String(64), index=True, unique=True)
    pass_hash = Column(String(128))
    # email = Column(String(64))

    # relations
    # roles = relationship("Role", uselist=True, back_populates="users")

    def __init__(self, password: Optional[str] = None, *args: Any, **kwargs: Any):
        super(User, self).__init__(*args, **kwargs)
        if password:
            self.password = password  # type: ignore

    @property
    def password(self) -> NoReturn:
        raise ValueError("password is write only")

    @password.setter
    def password(self, password: str) -> None:
        self.pass_hash = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        return generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pass_hash, password)

    def __repr__(self) -> str:  # pragma: nocover
        return f'<User {self.id}: {self.username}>'
