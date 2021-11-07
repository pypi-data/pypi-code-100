import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .chat import Chat
    from .base import TelegramObject
    from .user import User
    from .chat_invite_link import ChatInviteLink


class ChatJoinRequest(TelegramObject):
    """
    Represents a join request sent to a chat.
    """
    chat: Chat
    """Chat to which the request was sent"""
    from_user: User
    """User that sent the join request"""
    date: datetime.datetime
    """Date the request was sent in Unix time"""
    bio: Optional[str] = None
    """Optional. Bio of the user."""
    invite_link: ChatInviteLink
    """Optional. Chat invite link that was used by the user to send the join request"""
