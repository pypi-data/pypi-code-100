from typing import Union, Optional, List

from botco.contrib.session import Session
from .methods import (
    SendMessage,
    GetMe, LogOut, SendAudio, ForwardMessage, CopyMessage, GetUpdates, SendPhoto, SendDocument, SendVideo,
    SendAnimation, SendVoice, SendVideoNote, SendMediaGroup, SendLocation, EditMessageLiveLocation,
    StopMessageLiveLocation, SendVenue, SendContact, SendPoll, SendDice, SendChatAction
)
from .types import (
    MessageEntity,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply, UNSET, InputFile, Update
)
from .utils.helper import clean_locals


class Bot:
    def __init__(
            self, token: str, parse_mode: str = "HTML",
            session: Optional[Session] = None
    ):
        self.token = token
        self.parse_mode = parse_mode

        if session is None:
            session = Session()
        self.session = session

    def __call__(self, method):
        return self.session(self, method)

    @property
    def id(self):
        return int(self.token.split(":")[0])

    def get_updates(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Optional[int] = None,
            allowed_updates: Optional[List[str]] = None
    ) -> List[Update]:
        return self(GetUpdates(**clean_locals(locals())))

    def get_me(self):
        return self(GetMe())

    def logout(self):
        return self(LogOut())

    def send_message(
            self, chat_id: Union[int, str], text: str, parse_mode: Optional[str] = None,
            entities: List[MessageEntity] = None, disable_web_page_preview: bool = None,
            disable_notification: bool = None, reply_to_message_id: int = None,
            allow_sending_without_reply: bool = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup,
                                ReplyKeyboardRemove, ForceReply] = None
    ):
        return self(SendMessage(**clean_locals(locals())))

    def forward_message(
            self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int,
            disable_notification: Optional[bool] = None
    ):
        return self(ForwardMessage(**clean_locals(locals())))

    def copy_message(
            self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int, caption: Optional[str],
            parse_mode: Optional[str] = UNSET, caption_entities: Optional[List[MessageEntity]] = None,
            disable_notification: Optional[bool] = None, reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None, reply_markup: Optional[
                Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
            ] = None
    ):
        return self(CopyMessage(**clean_locals(locals())))

    def send_photo(
            self, chat_id: Union[int, str], photo: Union[InputFile, str], caption: Optional[str] = None,
            parse_mode: Optional[str] = UNSET, caption_entities: Optional[List[MessageEntity]] = None,
            disable_notification: Optional[bool] = None, reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[
                Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
    ):
        return self(SendPhoto(**clean_locals(locals())))

    def send_audio(
            self,
            chat_id: Union[int, str], audio: Union[InputFile, str], caption: Optional[str] = None,
            parse_mode: Optional[str] = UNSET, caption_entities: Optional[List[MessageEntity]] = None,
            duration: Optional[int] = None, performer: Optional[str] = None, title: Optional[str] = None,
            thumb: Optional[Union[InputFile, str]] = None, disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None, allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup,
                                         ReplyKeyboardRemove, ForceReply]] = None
    ):
        return self(SendAudio(**clean_locals(locals())))

    def send_document(
            self,
            chat_id: Union[int, str],
            document: Union[InputFile, str],
            thumb: Optional[Union[InputFile, str]] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = UNSET,
            caption_entities: Optional[List[MessageEntity]] = None,
            disable_content_type_detection: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[
                Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
    ):
        return self(SendDocument(**clean_locals(locals())))

    def send_video(
            self,
            chat_id: Union[int, str],
            video: Union[InputFile, str],
            duration: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            thumb: Optional[Union[InputFile, str]] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = UNSET,
            caption_entities: Optional[List[MessageEntity]] = None,
            supports_streaming: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[
                Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
            ] = None
    ):
        return self(SendVideo(**clean_locals(locals())))

    def send_animation(
            self,
            chat_id: Union[int, str],
            animation: Union[InputFile, str],
            duration: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            thumb: Optional[Union[InputFile, str]] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = UNSET,
            caption_entities: Optional[List[MessageEntity]] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[
                Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]
            ] = None
    ):
        return self(SendAnimation(**clean_locals(locals())))

    def send_voice(
            self,

    ):
        return self(SendVoice(**clean_locals(locals())))

    def send_video_note(self):
        return self(SendVideoNote(**clean_locals(locals())))

    def send_media_group(self):
        return self(SendMediaGroup(**clean_locals(locals())))

    def send_location(self):
        return self(SendLocation(**clean_locals(locals())))

    def edit_message_live_location(self):
        return self(EditMessageLiveLocation(**clean_locals(locals())))

    def stop_message_live_location(self):
        return self(StopMessageLiveLocation(**clean_locals(locals())))

    def send_venue(self):
        return self(SendVenue(**clean_locals(locals())))

    def send_contact(self):
        return self(SendContact(**clean_locals(locals())))

    def send_poll(self):
        return self(SendPoll(**clean_locals(locals())))

    def send_dice(self):
        return self(SendDice(**clean_locals(locals())))

    def send_chat_action(self):
        return self(SendChatAction(**clean_locals(locals())))
