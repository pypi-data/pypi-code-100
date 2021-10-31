# coding=utf-8
from mammut.visualization.simulator_widget import *


class Simulator:
    def __init__(
        self,
        users={},
        current_user=None,
        mammut_api=None,
        package=None,
        redis_memory=None,
        rooms={},
        chat_room=None,
        current_person_user=None,
        room_thoughts=None,
        supervisor=None,
    ):
        self.users = users
        self.current_user = current_user
        self.current_person_user = current_person_user
        self.mammut_api = mammut_api
        self.package = package
        self.redis_memory = redis_memory
        self.rooms = rooms
        self.chat_room = chat_room
        self.room_thoughts = room_thoughts
        self.supervisor = supervisor
        execution_mode = os.getenv("EXECUTION-MODE", "distributed")
        if execution_mode == "distributed":
            self.embedded = False
        else:
            self.embedded = True

    def get_simulator_widget(
        self,
        mammut_api_url,
        redis_address,
        redis_port,
        package_file,
        standard_spreadsheet_id,
        users_filename,
        users_rooms_spreadsheet_id,
        users_sheet_name,
        rooms_sheet_name,
        rooms_filename,
    ):
        return get_simulator_widget(
            self,
            mammut_api_url,
            redis_address,
            redis_port,
            package_file,
            standard_spreadsheet_id,
            users_filename,
            users_rooms_spreadsheet_id,
            users_sheet_name,
            rooms_sheet_name,
            rooms_filename,
        )
