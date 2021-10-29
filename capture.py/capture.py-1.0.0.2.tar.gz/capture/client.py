from typing import BinaryIO

from .lib.objects import *
from .lib.exceptions import *
from .threads import Threads
from .eventsource import SSE, Recall

import threading
import random

import requests
import json


class Client(Threads, Recall, SSE):
    def __init__(self, session_id: int = str(random.randint(1, 9999))):
        self.token = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "session-id": session_id,
            "x-user-agent": "14 Web/1 ru"
        }
        self.api = "https://capture.chat/api"
        Threads.__init__(self)
        Recall.__init__(self)
        SSE.__init__(self, self)

    def handle(self, data, event):
        return self.solve(data, event)

    def login_token(self, token: str):
        self.headers["X-Token"] = token
        self.token = token

    def get_topic_id(self, url: str):
        response = requests.get(f"{self.api}/link/preview?url={url}", headers=self.headers)
        topic_id = str(response.json()["topic_id"])
        if response.status_code != 200: CheckExceptions(response.json())
        else: return topic_id

    def get_notifications(self):
        response = requests.get(f"{self.api}/notification", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return Notifications(response.json()["items"]).Notifications

    def get_topic_users(self, topicId: str, count: int = 10):
        response = requests.get(f"{self.api}/topic/{topicId}/member?count={count}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return UserProfileList(response.json()["items"]).UserProfileList

    def get_user_topics(self, userId: str, count: int = 10):
        response = requests.get(f"{self.api}/user/{userId}/topic?count={count}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return TopicList(response.json()["items"]).TopicList

    def get_discover_topic(self, count: int = 10, type: str = "default"):
        if type == "default": api = f"{self.api}/topic/discover?count={count}"
        if type == "latest": api = f"{self.api}/topic/discover?count={count}"
        elif type == "trending": api = f"{self.api}/topic/discover/1582634058468904012?count={count}"
        elif type == "chats": api = f"{self.api}/topic/discover/1582658119463642908?count={count}"
        elif type == "topics": api = f"{self.api}/topic/discover/1582658869630172140?count={count}"
        response = requests.get(api)

        if response.status_code != 200: CheckExceptions(response.json())
        else:
            if type == "latest": return TopicList(response.json()["collections"]).TopicList
            else: return TopicList(response.json()["items"]).TopicList

    def get_topics(self, count: int = 10):
        response = requests.get(f"{self.api}/topic?count={count}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return TopicList(response.json()["items"]).TopicList

    def get_user_info(self, userId: str):
        response = requests.get(f"{self.api}/user/{userId}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return UserProfile(response.json()).UserProfile

    def get_trending_gif(self):
        response = requests.get(f"{self.api}/gifs/trending", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return Gifs(response.json()).Gifs

    def get_topic_photos(self, topicId: str, count: str = 50, reverse: bool = True):
        if reverse: reverse = "true"
        elif not reverse: reverse = "false"

        response = requests.get(f"{self.api}/topic/{topicId}/photo?count={count}&reverse={reverse}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return PhotoList(response.json()["items"]).PhotoList

    def get_topic_messages(self, topicId: str, count: int = 10):
        response = requests.get(f"{self.api}/topic/{topicId}/message?count={count}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return MessageList(response.json()["items"]).MessageList

    def search_mention_users(self, topicId: str, prefix: str = ""):
        response = requests.get(f"{self.api}/topic/{topicId}/mention/suggest?prefix={prefix}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return UserProfileList(response.json()["users"]).UserProfileList

    def send_message(self, topicId: str, message: str = None, replyMessage: str = None, photo: [BinaryIO, list] = None, gifId: str = None, gifProvider: str = None):
        links = []

        if photo:
            if isinstance(photo, list): photos = photo
            try:
                photo.__getattribute__("name")
                photos = [photo]
            except: TypeError("Photo should be BinaryIO!")
            for photo in photos:
                multipart = {'photo': (photo.__getattribute__("name"), photo), }
                response = requests.post(f"{self.api}/topic/{topicId}/message/photo", headers=self.headers, files=multipart)
                if response.status_code != 200: CheckExceptions(response.json())
                else: links.append(response.json()["photo"])

        data = {
            "text": message,
            "photos": links
        }

        if replyMessage: data["quote_message_id"] = replyMessage
        if gifId and gifProvider: data["gif_id"] = gifId; data["gif_provider"] = gifProvider

        data = json.dumps(data)
        response = requests.post(f"{self.api}/topic/{topicId}/message", headers=self.headers, data=data)
        if response.status_code != 200: return CheckExceptions(response.json())
        else: return Message(response.json()).Message

    def create_topic(self, bio: str, name: str, isChannel: bool = False, isPrivate: bool = False):
        data = json.dumps({
            "channel": isChannel,
            "private": isPrivate,
            "name": name,
            "content": bio
        })
        response = requests.post(f"{self.api}/topic", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_topic(self, topicId: str, bio: str = None, name: str = None, categoryId: int = 1, mute: bool = False, sound: bool = False):
        data = json.dumps({
            "category_id": categoryId,
            "name": name,
            "discription": bio
        })
        _data = json.dumps({"sound": sound, "mute": mute})
        requests.patch(f"{self.api}/topicId/{topicId}/settings", data=_data, headers=self.headers)
        response = requests.patch(f"{self.api}/topicId/{topicId}", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def login(self, email: str):
        response = requests.post(f"{self.api}/auth/?username={email}%40gmail.com")
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def delete_message(self, topicId: str, messageId: str):
        response = requests.delete(f"{self.api}/topic/{topicId}/message{messageId}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def leave_topic(self, topicId: str):
        response = requests.delete(f"{self.api}/topic/{topicId}/subscription", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def join_topic(self, topicId: str):
        response = requests.post(f"{self.api}/topic/{topicId}/subscription", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_profile(self, photo: BinaryIO = None, username: str = None, bio: str = None, location: str = None, status: bool = True):
        if photo is not None:
            multipart = {'photo': (photo.__getattribute__("name"), photo), }
            response = requests.post(f"{self.api}/user/me/photo", headers=self.headers, files=multipart)
            if response.status_code != 200: CheckExceptions(response.json())
            else: link = response.json()["photo"]

        data = json.dumps({
            "bio": bio,
            "location": location,
            "name": username,
            "online": status,
            "photo": link
        })
        response = requests.patch(f"{self.api}/user/me", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def sign_up(self, username):
        data = json.dumps({"username": username})
        response = requests.post(f"{self.api}/auth/username", data=data)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return NewAcc(response.json()).NewAcc

    def change_user_role(self, topicId: str, userId: str, role: str):
        data = json.dumps({"admin": role})
        response = requests.patch(f"{self.api}/topic/{topicId}/member/{userId}", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_message(self, topicId: str, messageId: str, newText: str):
        data = json.dumps({"text": newText})
        response = requests.patch(f"{self.api}/topic/{topicId}/message/{messageId}", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def ban(self, topicId: str, userId: str):
        response = requests.post(f"{self.api}/topic/{topicId}/ban{userId}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def report(self, userId: str, reason: str = "From Web"):
        data = {"reason": reason}

        if reason is None: data["comment"] = "Web"

        data = json.dumps(data)
        response = requests.post(f"{self.api}/user/{userId}/report", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def report_message(self, topicId: str, messageId: str, reason: str = "From Web"):
        data = {"reason": reason}
        if reason is None: data["comment"] = "Web"
        data = json.dumps(data)
        response = requests.post(f"{self.api}/topic/{topicId}/message/{messageId}", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def unban(self, topicId: str, userId: str):
        response = requests.delete(f"{self.api}/topic/{topicId}/ban/{userId}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def start_dm(self, userId: str):
        response = requests.post(f"{self.api}/dm/user/{userId}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def follow(self, topicId: str):
        response = requests.post(f"{self.api}/topic/{topicId}/follow", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def unfollow(self, topicId: str):
        response = requests.delete(f"{self.api}/topic/{topicId}/unfollow", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def search_topic(self, text: str):
        response = requests.get(f"{self.api}/topic/search/{text}", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return TopicList(response.json()).TopicList

    def unread(self, topicId: str):
        response = requests.delete(f"{self.api}/topic/{topicId}/unread", headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def start_typing_status(self, topicId: str, time: int = 5, status: str = "text", messageId: str = None):
        threading.Thread(target=self.send, args=(self._send_typing_status_, (self.headers, topicId, status, ), time)).start()
        if messageId: threading.Thread(target=self.send_edit, args=(self._when_typing_, topicId, messageId, )).start()


