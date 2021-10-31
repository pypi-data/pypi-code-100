# coding=utf-8
import datetime
import functools
from enum import Enum, auto
from mammut.common.storage.storage_manager import StorageManager
import requests
import json
import mammut
from functools import reduce


from mammut.common.util import StringEnum, RegionalSettingsType


class MicroExperience(StringEnum):
    call = "call"
    share = "share"
    web = "web"
    app = "app"
    postback = "postback"
    quickreply = "quickreply"


class WebviewSize(StringEnum):
    compact = "compact"
    tall = "tall"
    full = "full"


class UserType(StringEnum):
    supervisor = "supervisor"
    person = "person"
    normal = "normal"
    machine = "machine"
    facebook = "facebook-automatic"


class VerificationStatus(StringEnum):
    unverified = "unverified"
    verified = "verified"
    unknown = "unknown"


class Gender(StringEnum):
    male = "male"
    female = "female"
    other = "other"


class RoomType(StringEnum):
    group = "group"
    private = "private"


class PosiblePlacesFormat(StringEnum):
    textField = 0
    select = 1
    checkBox = 2
    video = 3
    image = 4
    url = 5


class CountryCodes(StringEnum):
    VE = "+58"
    CH = "+56"
    US = "+1"


class User:
    def __init__(
        self,
        first_name: str,
        last_name,
        nickname,
        main_phone_number: str,
        main_email: str,
        locale: RegionalSettingsType,
        gender: Gender,
        birthdate: datetime.date,
        verification_status: VerificationStatus,
        user_type: UserType,
        facebook_id: str = "",
        facebook_access_token: str = "",
        rooms: list = [],
        bot_name: str = "",
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.main_phone_number = main_phone_number
        self.main_email = main_email
        self.locale = locale
        self.gender = gender
        self.birthdate = birthdate
        self.verification_status = verification_status
        self.user_type = user_type
        self.facebook_id = facebook_id
        self.facebook_access_token = facebook_access_token
        self.verbs = {}
        self.rooms = rooms
        self.bot_name = bot_name
        self.id = None

    @classmethod
    def from_json(cls, api_user_json: {}):
        first_name = ""
        last_name = ""
        nickname = ""

        # Get names from proper noun structures

        if "name" in api_user_json.keys():
            first_name = api_user_json["name"]
        if "lastname" in api_user_json.keys():
            last_name = api_user_json["lastname"]
        if "nickname" in api_user_json.keys():
            nickname = api_user_json["nickname"]

        id = api_user_json["id"]

        main_phone_number = ""
        if "main-phone-number" in api_user_json.keys():
            main_phone_number = api_user_json["main-phone-number"]
        main_email = ""
        if "main-email" in api_user_json.keys():
            main_email = api_user_json["main-email"]
        locale = ""
        if "locale" in api_user_json.keys():
            temp_local = api_user_json["locale"].lower()
            if temp_local == "sp":
                temp_local = "es"
            locale = RegionalSettingsType(temp_local)
        gender = ""
        if "gender" in api_user_json.keys():
            gender = Gender[api_user_json["gender"]]
        birthdate = None
        if "birthdate" in api_user_json.keys():
            birthdate = mammut.str_parse_datetime(api_user_json["birthdate"]).date()
        verification_status = None
        if "verification-status" in api_user_json.keys():
            verification_status = VerificationStatus[
                api_user_json["verification-status"]
            ]
        user_type = None
        if "user-type" in api_user_json.keys():
            user_type = UserType(api_user_json["user-type"])

        facebook_id = ""
        if "facebook-id" in api_user_json.keys():
            facebook_id = api_user_json["facebook-id"]

        facebook_access_token = ""
        if "facebook-access-token" in api_user_json.keys():
            facebook_access_token = api_user_json["facebook-access-token"]

        rooms = []
        if "chat-in" in api_user_json.keys():
            for room in api_user_json["chat-in"]["room"]:
                rooms.append(Room.from_json(room))
        elif "create" in api_user_json.keys():
            for room in api_user_json["create"]["room"]:
                rooms.append(Room.from_json(room))

        bot_name = ""
        if "bot-name" in api_user_json.keys():
            bot_name = api_user_json["bot-name"]

        user = User(
            first_name,
            last_name,
            nickname,
            main_phone_number,
            main_email,
            locale,
            gender,
            birthdate,
            verification_status,
            user_type,
            facebook_id,
            facebook_access_token,
            rooms,
            bot_name,
        )
        user.id = id
        return user

    def to_json(self):
        data = {}
        if self.main_phone_number != "":
            data["main-phone-number"] = self.main_phone_number
        data["main-email"] = self.main_email
        if self.locale is not "":
            data["locale"] = self.locale.value
        if self.gender is not "":
            data["gender"] = self.gender.value
        if self.birthdate is not None:
            data["birthdate"] = self.birthdate.strftime(mammut.LOCAL_DATE_FORMATTER)
        if self.verification_status is not None:
            data["verification-status"] = self.verification_status.value
        if self.user_type is not None:
            data["user-type"] = self.user_type.value
        if self.facebook_id != "":
            data["facebook-id"] = self.facebook_id
        if self.facebook_access_token != "":
            data["facebook-access-token"] = self.facebook_access_token
        data["name"] = self.first_name
        if self.last_name is not None:
            data["lastname"] = self.last_name
        if self.bot_name is not "":
            data["bot-name"] = self.bot_name

        if self.id is not None:
            data["id"] = self.id

        return data

    def add_verb(
        self,
        scoped: bool,
        id: int,
        title: str,
        micro_experience: str,
        phone_number: str,
        url: str,
        url_parameters: str,
        payload: str,
        image: str,
        webview_size: str,
        knowledge_graph,
    ):
        verb = Verb(
            self,
            scoped,
            id,
            title,
            micro_experience,
            phone_number,
            url,
            url_parameters,
            payload,
            image,
            webview_size,
            knowledge_graph,
        )
        self.verbs[id] = verb
        return verb

    def has_verb(self, id: int):
        return id in self.verbs

    def get_verb(self, id: str):
        return self.verbs[id]


class VerbInstance:
    def __init__(
        self,
        verb,
        title: str,
        micro_experience: MicroExperience,
        phone_number: str = None,
        url: str = None,
        url_parameters: str = None,
        payload: str = None,
        image: str = None,
        webview_size: str = None,
        vertex_title: str = None,
        vertex_index: str = None,
    ):
        self.verb = verb
        self.title = title
        self.micro_experience = micro_experience
        self.url = url
        if url_parameters:
            if isinstance(url_parameters, list):
                self.url = self.url.format(*url_parameters)
            else:
                self.url = self.url.format(url_parameters)
        self.phone_number = phone_number
        self.payload = payload
        self.image = image
        self.webview_size = webview_size
        self.api_id = 0
        self.vertex_title = vertex_title
        self.vertex_index = vertex_index


class VerbDefinitionType(Enum):
    Singleton = auto()
    OneInstancePerMainVertex = auto()
    MultipleInstancesPerMainVertex = auto()


class Verb:
    def __init__(
        self,
        user: User,
        scoped: bool,
        id: int,
        title: str,
        str_micro_experience: str,
        phone_number: str,
        url: str,
        url_parameters: str,
        payload: str,
        image: str,
        webview_size: str,
        knowledge_graph,
    ):
        def add_error_of_invalid_button(error_msg, invalid_tokens):
            self.valid = False
            invalid_tokens_str = functools.reduce(
                lambda l, r: l + r, invalid_tokens, ""
            )
            error_msg = "Invalid button: " + error_msg + f". Id = {self.id}"
            if len(invalid_tokens) > 0:
                error_msg = error_msg + f". Invalid tokens: {invalid_tokens_str}"
            self.errors.append(error_msg)

        self.valid = True
        self.errors = []
        self.user = user
        self.scoped = scoped
        self.id = id
        self.title = title
        self.str_micro_experience = str_micro_experience
        self.url = url
        self.url_parameters = url_parameters
        self.phone_number = phone_number
        self.payload = payload
        self.image = image
        self.webview_size_str = webview_size
        self.webview_size = None
        self.knowledge_graph = knowledge_graph
        self.definition_type = VerbDefinitionType.Singleton
        self.singleton_instance = None
        self.instances = {}

        if self.str_micro_experience in list(MicroExperience.__members__):
            self.micro_experience = MicroExperience(self.str_micro_experience)
        else:
            self.micro_experience = MicroExperience.share
            add_error_of_invalid_button("has invalid micro-experience", [])
        self.tokenized_title = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
            self.title, False, self.user.locale.value, self.knowledge_graph
        )
        self.has_variable_title = len(self.tokenized_title.variables) > 0
        if len(self.tokenized_title.invalid_variables) > 0:
            add_error_of_invalid_button(
                "has a invalid variable in the title",
                self.tokenized_title.invalid_variables,
            )
        if self.micro_experience == MicroExperience.call:
            self.tokenized_phone_number = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
                self.phone_number, False, self.user.locale.value, self.knowledge_graph
            )
            self.has_variable_phone_number = (
                len(self.tokenized_phone_number.variables) > 0
            )
            if self.tokenized_phone_number.contains_invalid_variables():
                add_error_of_invalid_button(
                    "has a invalid variable in the phone number",
                    self.tokenized_phone_number.invalid_variables,
                )
        elif (
            self.micro_experience == MicroExperience.web
            or self.micro_experience == MicroExperience.app
        ):
            self.tokenized_url = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
                self.url, False, self.user.locale.value, self.knowledge_graph
            )
            self.has_variable_url = len(self.tokenized_url.variables) > 0
            if self.tokenized_url.contains_invalid_variables():
                add_error_of_invalid_button(
                    "has a invalid variable in the url",
                    self.tokenized_url.invalid_variables,
                )
            self.tokenized_url_parameters = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
                self.url_parameters, False, self.user.locale.value, self.knowledge_graph
            )
            self.has_variable_url_parameters = (
                len(self.tokenized_url_parameters.variables) > 0
            )
            if self.tokenized_url_parameters.contains_invalid_variables():
                add_error_of_invalid_button(
                    "has a invalid variable in the url parameters",
                    self.tokenized_url_parameters.invalid_variables,
                )

            if self.webview_size_str in list(WebviewSize.__members__):
                self.webview_size = WebviewSize(self.webview_size_str)

        elif (
            self.micro_experience == MicroExperience.postback
            or self.micro_experience == MicroExperience.quickreply
        ):
            self.tokenized_payload = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
                self.payload, False, self.user.locale.value, self.knowledge_graph
            )
            self.has_variable_payload = len(self.tokenized_payload.variables) > 0
            if self.tokenized_payload.contains_invalid_variables():
                add_error_of_invalid_button(
                    "has a invalid variable in the payload",
                    self.tokenized_payload.invalid_variables,
                )
            if self.micro_experience == MicroExperience.quickreply:
                self.tokenized_image = self.knowledge_graph.tokenizer.tokenize_corpus_entry(
                    self.image, False, self.user.locale.value, self.knowledge_graph
                )
                self.has_variable_image = len(self.tokenized_image.variables) > 0
                if self.tokenized_image.contains_invalid_variables():
                    add_error_of_invalid_button(
                        "has a invalid variable in the image",
                        self.tokenized_image.invalid_variables,
                    )


class Issue:
    def __init__(
        self,
        room_id,
        custom_code=None,
        caused_by=None,
        issue_type=None,
        machine_id=None,
        id=None,
        causative_connected=None,
        resolution_text=None,
        causative_id=None,
        issue_state=None,
    ):
        self.room_id = room_id
        self.custom_code = custom_code
        self.caused_by = caused_by
        self.issue_type = issue_type
        self.machine_id = machine_id
        self.id = id
        self.causative_connected = causative_connected
        self.resolution_text = resolution_text
        self.causative_id = causative_id
        self.issue_state = issue_state

    def to_json(self):
        data = {}
        data["creation-date"] = "now"
        data["issue-state"] = self.issue_state
        data["resolution-text"] = self.resolution_text
        data["issue-type"] = self.issue_type
        data["custom-code"] = self.custom_code
        data["machine-id"] = self.machine_id
        data["room-id"] = self.room_id
        data["causative-connected"] = self.causative_connected
        return data

    @classmethod
    def from_json(cls, issue_json: {}):
        room_id = None
        if "room-id" in issue_json.keys():
            room_id = issue_json["room-id"]
        custom_code = None
        if "custom-code" in issue_json.keys():
            custom_code = issue_json["custom-code"]
        caused_by = None
        if "caused-by" in issue_json.keys():
            caused_by = issue_json["caused-by"]
        issue_type = None
        if "issue-type" in issue_json.keys():
            issue_type = issue_json["issue-type"]
        machine_id = None
        if "machine-id" in issue_json.keys():
            machine_id = issue_json["machine-id"]
        id = None
        if "id" in issue_json.keys():
            id = issue_json["id"]
        causative_connected = None
        if "causative-connected" in issue_json.keys():
            causative_connected = issue_json["causative-connected"]
        resolution_text = None
        if "resolution-text" in issue_json.keys():
            resolution_text = issue_json["resolution-text"]
        causative_id = None
        if "causative-id" in issue_json.keys():
            causative_id = issue_json["causative-id"]
        issue_state = None
        if "issue-state" in issue_json.keys():
            issue_state = issue_json["issue-state"]
        issue = Issue(
            room_id,
            custom_code,
            caused_by,
            issue_type,
            machine_id,
            id,
            causative_connected,
            resolution_text,
            causative_id,
            issue_state,
        )
        return issue


class Thought:
    def __init__(self, user_id, room_id, text, creation_date, issue=None):
        self.user_id = user_id
        self.room_id = room_id
        self.text = text
        self.creation_date = creation_date
        self.issue = issue

    def to_json(self):
        data = {}
        data["text"] = self.text
        data["creation-date"] = self.creation_date
        data["in@room"] = {"id": self.room_id}
        return data

    @classmethod
    def from_json(cls, api_thought_json: {}):

        room_id = api_thought_json["in"]["room"][0]["id"]
        text = api_thought_json["text"]
        creation_date = api_thought_json["creation-date"]
        user = User.from_json(api_thought_json["send-by"]["user"][0])
        issue = None
        if "cause" in api_thought_json.keys():
            issue = Issue.from_json(api_thought_json["cause"]["issue"][0])
            print("isuee from thougth", Issue.__dict__)

        thought = Thought(user.id, room_id, text, creation_date, issue)

        return thought


class Room:
    def __init__(
        self,
        title,
        room_type: RoomType,
        creation_date,
        created_by: User = None,
        url="",
        custom_code="",
        room_id=None,
        user_members: list = [],
    ):
        self.title = title
        self.room_type = room_type
        self.creation_date = creation_date
        self.id = room_id
        self.created_by = created_by
        self.members = user_members
        self.url = url
        self.custom_code = custom_code

    @classmethod
    def from_json(cls, api_room_json: {}):
        room_id = api_room_json["id"]

        users = []
        if "has" in api_room_json.keys():
            for user_member in api_room_json["has"]["user"]:
                users.append(User.from_json(user_member))
        creation_date = ""
        if "creation-date" in api_room_json.keys():
            creation_date = api_room_json["creation-date"]
        created_by = None
        if "create-by" in api_room_json.keys():
            created_by = User.from_json(api_room_json["create-by"]["user"][0])
        title = ""
        if "title" in api_room_json.keys():
            title = api_room_json["title"]
        room_type = ""
        if "room-type" in api_room_json.keys():
            room_type = api_room_json["room-type"]
        url = ""
        if "url" in api_room_json.keys():
            url = api_room_json["url"]
        custom_code = ""
        if "custom-code" in api_room_json.keys():
            custom_code = api_room_json["custom-code"]

        return Room(
            title=title,
            room_type=room_type,
            creation_date=creation_date,
            created_by=created_by,
            url=url,
            custom_code=custom_code,
            room_id=room_id,
            user_members=users,
        )

    def to_json(self):

        data = {}
        data["room-type"] = self.room_type.value
        data["creation-date"] = self.creation_date
        data["title"] = self.title
        data["url"] = self.url
        data["custom-code"] = self.custom_code
        contain = []
        contain.append({"deleted": False})
        data["contain"] = contain
        return data


class CalendarCustomValues:
    def __init__(
        self, name: str, value: list, value_type: PosiblePlacesFormat, mandatory: bool
    ):
        self.name = name
        self.value = value
        self.value_type = value_type
        self.mandatory = mandatory

    def to_json(self):
        data = {}
        data[self.name] = {}
        data[self.name]["value"] = self.value
        data[self.name]["type"] = self.value_type
        data[self.name]["mandatory"] = self.mandatory
        return data


class Calendar:
    def __init__(
        self,
        user_id: str,
        mammut_user: User,
        title: str,
        possible_places: list,
        possible_places_format: PosiblePlacesFormat,
        possible_regional_settings: RegionalSettingsType,
        custom_fields: list,
        reminder_text_templates: dict,
        country_code: str,
    ):
        self.user_id = user_id
        self.mammut_user = mammut_user
        self.title = title
        self.possible_places = possible_places
        self.possible_places_format = possible_places_format
        self.possible_regional_settings = possible_regional_settings
        self.custom_fields = custom_fields
        self.reminder_text_templates = reminder_text_templates
        self.country_code = country_code

    def escape_curly_brakets_in_dict(self, data_dict):
        serialized = json.dumps(data_dict)
        return serialized

    def to_json(self):
        data = {}
        data["tittle"] = self.title
        data["possible-places"] = self.possible_places
        data["possible-places-format"] = self.possible_places_format
        data["custom-data-template"] = self.escape_curly_brakets_in_dict(
            self.custom_fields
        )
        data["handle-by@user"] = {"id": self.mammut_user.id}
        data["reminder-text-templates"] = self.escape_curly_brakets_in_dict(
            self.reminder_text_templates
        )
        data["possible-regional-settings"] = self.possible_regional_settings
        data["country-code"] = self.country_code
        return data


class Request:

    mammutUrl = "https://372aab09.ngrok.io"
    verb_path = "{mammutURL}/app:mammut-1/graph/user:{userId}/can"
    fixed_user_path = (
        "{mammutURL}/app:mammut-1/fixed-vertex?type-name=user&config-id=mammut&depth=2"
    )
    post_user_path = "{mammutURL}/app:mammut-1/graph/user"
    post_room_path = "{mammutURL}/app:mammut-1/graph/user:{userId}/create"
    get_user_path = "{mammutURL}/app:mammut-1/graph:2/user:{userId}"
    get_user_by_mail_path = "{mammutURL}/app:mammut-1/unique-vertex?type-name=user&property-name=main-email&property-value={userMail}&depth=2"
    get_room_path = "{mammutURL}/app:mammut-1/graph:2/room:{roomId}"
    post_thought_path = "{mammutURL}/app:mammut-1/graph/user:{userId}/send:=thought"
    post_issue_update_path = '{mammutURL}/app:mammut-1/graph/issue:{issueId}?resolution-text="{message}";issue-state="close";resolved-by@user:{"id":{supervisorId}} '
    post_issue_remove_halted_path = "{mammutURL}/app:mammut-1/graph/issue"
    get_last_thought_path = "{mammutURL}/app:mammut-1/graph:2/user:{userId}/send::thought?creation-date.last(1)"
    get_thoughts_path = "{mammutURL}/app:mammut-1/graph:2/user:{userId}/send::thought?creation-date.last(10)"
    get_room_thoughts_path = "{mammutURL}/app:mammut-1/graph:2/room:{roomId}/with::thought?creation-date.last(10)"
    get_room_thoughts_path_since = '{mammutURL}/app:mammut-1/graph:2/room:{roomId}/with::thought?creation-date.since("{since}")'
    post_video_path = "{mammutURL}/app:mammut-1/graph/video"
    post_calendar_path = "{mammutURL}/app:mammut-1/graph/user:{userId}/own:=calendar"
    get_videos_path = "{mammutURL}/app:mammut-1/graph/user:{userId}/own::video"
    post_compilation_path = "{mammutURL}/app:mammut-1/actions/compile"
    get_vertex_by_unique_property_path = "{mammutURL}/app:mammut-1/unique-vertex?type-name={vertex}&property-name={prop_name}&property-value={prop_value}&depth=1"

    def __init__(self, mammut_url: str):
        self.mammutUrl = mammut_url

    def post_user(self, user: User = None, payload=None):

        if payload == None:
            data = user.to_json()
        else:
            data = payload
        response = self.post_request(self.post_user_path, data)

        if response is not None:
            # Get user id
            response_json = response.json()

            if response_json["status"] != "Failed":
                for result in response_json["taskResult"]:
                    if result["affectedElementName"] == "user":
                        print(
                            "efected elemnt id on user creation",
                            result["affectedElementId"],
                        )
                        created_user_id = result["affectedElementId"]
                        if user is not None:
                            user.id = created_user_id
                        break
                return created_user_id
            else:
                print("Response status for user creation is FAILED")
                return None
        else:
            print("Error saving User.")

    def post_room(
        self, room: Room = None, payload=None, data_is_json=False, creator=None
    ):
        if payload is not None:
            data = payload
            user_id = self.get_fixed_mammut().id
        else:
            data = room.to_json()
            user_id = room.created_by.id
        if creator is not None:
            user_id = creator.id
        url = self.post_room_path.replace("{userId}", str(user_id))
        response = self.post_request(url, data, data_is_json)

        created_room_id = None
        if response is not None:
            response_json = response.json()
            print(response_json["status"])

            if response_json["status"] != "Failed":
                for result in response_json["taskResult"]:
                    if result["affectedElementName"] == "room":
                        created_room_id = result["affectedElementId"]
                        if room is not None:
                            room.id = created_room_id
                        break
        else:
            print("Error creating room.")

        if payload is not None:
            return created_room_id
        else:
            return room

    def post_thought(self, thought: Thought):
        data = thought.to_json()
        url = self.post_thought_path.replace("{userId}", str(thought.user_id))
        response = self.post_request(url, data).json()
        return response

    def post_totblt_resolution(self, issue: Issue, supervisor: User, message: str):
        data = {}
        url = (
            self.post_issue_update_path.replace("{issueId}", str(issue.id))
            .replace("{supervisorId}", str(supervisor.id))
            .replace("{message}", message)
        )
        print(url)
        response = self.post_request(url, data).json()
        return response

    def post_remove_halted_mark_issue(self, issue: Issue):
        data = issue.to_json()
        url = self.post_issue_remove_halted_path
        response = self.post_request(url, data)
        return response

    def post_video(self, video_name, video_url, user_id):
        data = {
            "title": video_name,
            "url": video_url,
            "belong-to@user": {"id": user_id},
        }
        url = self.post_video_path
        response = self.post_request(url, data)

        if response is not None:
            response_json = response.json()
            if response_json["status"] != "Failed":
                for result in response_json["taskResult"]:
                    if result["affectedElementName"] == "video":
                        print("Created video", result["affectedElementId"])
                        break

        else:
            print("Error creating Video.")
        return response

    def post_calendar(self, calendar: Calendar):
        data = calendar.to_json()
        url = self.post_calendar_path.replace("{userId}", str(calendar.user_id))
        response = self.post_request(url, data).json()
        return response

    def post_verb(self, verb_def: Verb):

        verb_instances = []

        # Get verb instances depending the type of definition
        if (
            verb_def.definition_type
            == VerbDefinitionType.MultipleInstancesPerMainVertex
        ):
            for vil in verb_def.instances.values():
                verb_instances.extend(vil)
        elif verb_def.definition_type == VerbDefinitionType.OneInstancePerMainVertex:
            verb_instances.extend(verb_def.instances.values())
        else:
            verb_instances.insert(0, verb_def.singleton_instance)

        url = self.verb_path.replace("{userId}", str(verb_def.user.id))

        # post verb instances
        for verb in verb_instances:

            data = {}
            data["title"] = verb.title
            data["micro-experience"] = verb.micro_experience.value
            if verb.micro_experience == MicroExperience.call:
                data["phone-number"] = verb.phone_number
            elif (
                verb.micro_experience == MicroExperience.web
                or verb.micro_experience == MicroExperience.app
            ):
                data["url"] = verb.url
                if verb.webview_size:
                    data["webview-size"] = verb.webview_size.value
            elif (
                verb.micro_experience == MicroExperience.postback
                or verb.micro_experience == MicroExperience.quickreply
            ):
                if verb.payload:
                    data["payload"] = verb.payload
                if verb.micro_experience == MicroExperience.quickreply:
                    data["content-type"] = "text"
                    if verb.image:
                        data["image-url"] = verb.image

            response = self.post_request(url, data)

            if response is not None:
                # Get verb id
                response_json = response.json()

                for result in response_json["taskResult"]:
                    if result["affectedElementName"] == "verb":
                        verb.api_id = result["affectedElementId"]
            else:
                print("Error saving Verb.")

    def get_user(self, user_id):

        url = self.get_user_path.replace("{userId}", str(user_id))

        response = self.get_request(url)

        if response is None:
            print("Error getting user " + str(user_id))

        else:
            response_json = response.json()

            if (
                "user" in response_json["data"].keys()
                and len(response_json["data"]["user"]) > 0
            ):

                # Get first user response
                user = User.from_json(response_json["data"]["user"][0])
                return user
            else:
                print("No user found for: " + str(user_id))

    def get_user_by_mail(self, user_mail, raw_user=False):

        url = self.get_user_by_mail_path.replace("{userMail}", str(user_mail))

        response = self.get_request(url)

        if response is None:
            print("Error getting user " + str(user_mail))

        else:
            response_json = response.json()

            if response_json["status"] != "Failed":
                if (
                    "user" in response_json["data"].keys()
                    and len(response_json["data"]["user"]) > 0
                ):

                    # Get first user response
                    if raw_user:
                        user = response_json["data"]["user"][0]
                    else:
                        user = User.from_json(response_json["data"]["user"][0])
                    return user
                else:
                    print("No user found for: " + str(user_mail))
                    return None
            else:
                print("No user found for: " + str(user_mail))
                return None

    def get_last_sent_thought(self, user_id):

        thought = None
        url = self.get_last_thought_path.replace("{userId}", str(user_id))

        response = self.get_request(url)

        if response is None:
            print("Error getting user last thought: " + str(user_id))
        else:
            response_json = response.json()
            if (
                "thought" in response_json["data"].keys()
                and len(response_json["data"]["thought"]) > 0
            ):
                thought = Thought.from_json(response_json["data"]["thought"][0])
            else:
                print("No thought sent for: " + str(user_id))

        return thought

    def get_thoughts(self, id, from_type="User"):

        thoughts = list()
        if from_type == "User":
            url = self.get_thoughts_path.replace("{userId}", str(id))
        elif from_type == "Room":
            url = self.get_room_thoughts_path.replace("{roomId}", str(id))
            print(url)

        response = self.get_request(url)

        if response is None:
            print("Error getting user last thought: " + str(id))
        else:
            response_json = response.json()
            if (
                "thought" in response_json["data"].keys()
                and len(response_json["data"]["thought"]) > 0
            ):
                for thought_response in response_json["data"]["thought"]:
                    thoughts.append(Thought.from_json(thought_response))
            else:
                print("No thought sent for " + from_type + ": " + str(id))

        return thoughts

    def get_thoughts_since(self, id, since_date):
        thoughts = list()
        url = self.get_room_thoughts_path_since.replace("{roomId}", str(id))
        url = url.replace("{since}", since_date)
        response = self.get_request(url)
        if response is None:
            print("Error getting user last thought: " + str(id))
        else:
            response_json = response.json()
            if (
                "thought" in response_json["data"].keys()
                and len(response_json["data"]["thought"]) > 0
            ):
                for thought_response in response_json["data"]["thought"]:
                    thoughts.append(Thought.from_json(thought_response))
            else:
                print("No thought sent for room with since filter")

        return thoughts

    def get_shared_room_id(self, user: User, mammut_user_id):

        room_found = None
        for user_room in user.rooms:
            # needs to get all info
            room = self.get_room(user_room.id)

            if room.created_by.id == mammut_user_id:
                return room
            else:
                for user in room.members:
                    if user.id == mammut_user_id:
                        return room

        return room_found

    def get_fixed_mammut(self):
        response = self.get_request(self.fixed_user_path)

        if response is None:
            print("Error getting fixed mammut user")

        else:
            response_json = response.json()

            # Get first user response
            user = User.from_json(response_json["data"]["user"][0])
            return user

    def get_room(self, room_id):
        room = None
        url = self.get_room_path.replace("{roomId}", str(room_id))
        response = self.get_request(url)

        if response is None:
            print("Error getting room: " + str(room_id))
        else:
            response_json = response.json()

            if (
                "room" in response_json["data"].keys()
                and len(response_json["data"]["room"]) > 0
            ):
                room = Room.from_json(response_json["data"]["room"][0])
            else:
                print("No room found for: " + str(room_id))

        return room

    def get_videos(self, mammut_id):
        videos = []
        url = self.get_videos_path.replace("{userId}", str(mammut_id))
        response = self.get_request(url)

        if response is None:
            print("Error getting videos form user: " + str(mammut_id))
        else:
            response_json = response.json()
            print(response_json)

            if (
                "video" in response_json["data"].keys()
                and len(response_json["data"]["video"]) > 0
            ):
                videos = response_json["data"]["video"]
            else:
                print("No videos found for: " + str(mammut_id))

        return videos

    def post_request(self, request_path: str, data: {}, data_is_json=False):
        url = request_path.replace("{mammutURL}", self.mammutUrl)
        if data_is_json:
            json_data = data
        else:
            json_data = json.dumps(data)
        response = requests.post(
            url, data=json_data, headers={"Content-type": "application/json"}
        )

        if response.status_code != 200:
            print("Error connecting to Mammut api. Code: " + str(response.status_code))

        return response

    def get_request(self, request_path: str):
        url = request_path.replace("{mammutURL}", self.mammutUrl)
        response = requests.get(url)

        if response.status_code != 200:
            print("Error connecting to Mammut api. Code: " + str(response.status_code))

        return response

    def post_compilation(self, payload):
        response = self.post_request(self.post_compilation_path, payload, True)
        if response is not None:
            if response.status_code == "200":
                return 200
            elif response.status_code == "503":
                return 503
            else:
                print("Unknown respose status code received")
                return int(response.status_code)
        else:
            print("Error posting compilation to API.")

    def get_unique_vertex(self, vertex: str, prop_name: str, prop_value: str):
        str_replacements_dict = {
            "{vertex}": vertex,
            "{prop_name}": prop_name,
            "{prop_value}": prop_value,
        }
        rest_url = self.get_vertex_by_unique_property_path.replace(
            "{mammutURL}", self.mammutUrl
        )
        for i, j in str_replacements_dict.items():
            rest_url = rest_url.replace(i, j)

        api_response = self.get_request(rest_url)

        if api_response is None:
            return {"error": {"message": "Error communicating with Mammut API"}}
        else:
            api_response_json = api_response.json()
            if (
                api_response_json["status"] == "Success"
                and len(api_response_json["data"][vertex]) > 0
            ):
                user = api_response_json["data"][vertex][0]
                return user
            else:
                return {}


class UsersLoader:
    DEFAULT_USERS_LOADER_START_CELL = "A1"
    DEFAULT_USERS_LOADER_START_COLUMN = "A"
    DEFAULT_USERS_LOADER_START_ROW = "1"
    DEFAULT_USERS_LOADER_END_CELL = "E"
    DEFAULT_MAIN_EMAIL_COLUMN_NAME = "main-email"
    DEFAULT_ID_COLUMN_NAME = "id"
    storage_manager = StorageManager()

    def __init__(self, spreadsheet_id: str, sheet_name: str, mammut_api: Request):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name, self.end_cell = sheet_name.split("-")
        self.mammut_api = mammut_api
        self.users_dataframe = None
        self.users_list = []

    def get_users_dataframe(self):

        self.users_dataframe = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.sheet_name,
            UsersLoader.DEFAULT_USERS_LOADER_START_COLUMN,
            UsersLoader.DEFAULT_USERS_LOADER_START_ROW,
            self.end_cell,
        )

    def create_user(self, df_row):
        user = None
        payload = {col: df_row[col] for col in df_row.keys()}
        user_response = self.mammut_api.post_user(user, payload)
        if user_response is not None:
            payload["id"] = user_response
            return payload
        else:
            print("error creating user with payload")
            return None

    # TODO: al hacer el post de user deberia ahcer get del mismo para tener todos los campos??o con agregar los mismos del sheet base basta?
    def check_users(self):
        for index, row in self.users_dataframe.iterrows():
            raw_user = self.mammut_api.get_user_by_mail(
                row[UsersLoader.DEFAULT_MAIN_EMAIL_COLUMN_NAME], raw_user=True
            )
            if raw_user == None:
                raw_user = self.create_user(row)
                if raw_user is not None:
                    self.users_list.append(raw_user)
            else:
                self.users_list.append(raw_user)
        return self.users_list

    def save_users(self):
        sheet_titles = list()
        all_users_keys = list(map(lambda user: list(user.keys()), self.users_list))
        all_users_keys = reduce((lambda x, user_keys: x + user_keys), all_users_keys)
        unique_keys = list(set(all_users_keys))
        sheet_titles = sheet_titles + unique_keys

        user_keys = sheet_titles
        row = []
        rows = []
        rows.append(sheet_titles)
        for user in self.users_list:
            for key in user_keys:
                user_json = user
                if key in user_json:
                    if isinstance(user_json[key], dict):
                        row.append(json.dumps(user_json[key]))
                    else:
                        row.append(user_json[key])
                else:
                    row.append("empty")
            rows.append(row)
            row = []
        temporal_sheet_name = self.sheet_name + "-result"
        temporal_sheets = self.storage_manager.get_temporal_sheets_from_new_to_old(
            self.spreadsheet_id, temporal_sheet_name
        )
        if len(temporal_sheets) > 0:
            for ts in temporal_sheets:
                self.storage_manager.delete_sheet(self.spreadsheet_id, ts[0])
        dump_sheet_title = self.storage_manager.create_temporal_new_sheet(
            self.spreadsheet_id, temporal_sheet_name
        )
        dump_range_name = (
            dump_sheet_title + "!" + UsersLoader.DEFAULT_USERS_LOADER_START_CELL
        )
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id,
            dump_sheet_title,
            rows,
            UsersLoader.DEFAULT_USERS_LOADER_START_ROW,
            UsersLoader.DEFAULT_USERS_LOADER_START_COLUMN,
        )

    def load_users(self):
        self.get_users_dataframe()
        self.check_users()
        self.save_users()


class RoomsCreator:
    DEFAULT_ROOM_CREATOR_START_CELL = "A1"
    DEFAULT_ROOM_CREATOR_START_COLUMN = "A"
    DEFAULT_ROOM_CREATOR_START_ROW = "1"
    DEFAULT_ROOM_CREATOR_END_CELL = "F"
    storage_manager = StorageManager()

    def __init__(self, mammut: User, spreadsheet_id, mammut_api):
        self.mammut = mammut
        self.spreadsheet_id = spreadsheet_id
        self.rooms_dataframe = None
        self.rooms = list()
        self.mammut_api = mammut_api

    def get_rooms(self, sheet_title):
        self.rooms_dataframe = self.storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            sheet_title,
            RoomsCreator.DEFAULT_ROOM_CREATOR_START_COLUMN,
            RoomsCreator.DEFAULT_ROOM_CREATOR_START_ROW,
            RoomsCreator.DEFAULT_ROOM_CREATOR_END_CELL,
        )

    def create_rooms(self, character_limit=None):
        date = mammut.get_str_format_timezone_aware_datetime_now()
        for index, row in self.rooms_dataframe.iterrows():
            title = row.title if not character_limit else row.title[:character_limit]
            room = Room(
                title, RoomType.group, date, self.mammut, row.url, row.custom_code
            )
            self.rooms.append(room)
            self.mammut_api.post_room(room)

    def save_rooms(self, sheet_title):
        sheet_titles = ["id", "title"]
        row = []
        rows = []
        rows.append(sheet_titles)
        for room in self.rooms:
            row.append(room.id)
            row.append(room.title)
            row.append(room.url)
            row.append(room.custom_code)
            rows.append(row)
            row = []
        temporal_sheet_name = sheet_title + "-rooms"
        temporal_sheets = self.storage_manager.get_temporal_sheets_from_new_to_old(
            self.spreadsheet_id, temporal_sheet_name
        )
        if len(temporal_sheets) > 0:
            for ts in temporal_sheets:
                self.storage_manager.delete_sheet(self.spreadsheet_id, ts[0])
        dump_sheet_title = self.storage_manager.create_temporal_new_sheet(
            self.spreadsheet_id, temporal_sheet_name
        )
        dump_range_name = (
            dump_sheet_title + "!" + UsersLoader.DEFAULT_USERS_LOADER_START_CELL
        )
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id,
            dump_sheet_title,
            rows,
            UsersLoader.DEFAULT_USERS_LOADER_START_ROW,
            UsersLoader.DEFAULT_USERS_LOADER_START_COLUMN,
        )

    def activate(self, sheet_title):
        self.get_rooms(sheet_title)
        self.create_rooms()
        self.save_rooms(sheet_title)
