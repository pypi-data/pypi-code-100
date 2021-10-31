from mammut.common.mammut_api import *
from mammut.common.corpus import *
from ipywidgets import *


def to_sp_string(valid: bool):
    if valid:
        return "está correcto."
    else:
        return "presenta errores."


def load_users(simulator_obj, users_filename: str):
    users_file = open(users_filename, "r")
    simulator_obj.users = json.loads(users_file.read())
    users_file.close()


def save_users(simulator_obj, users_filename: str):
    print("users", simulator_obj.users)
    users_file = open(users_filename, "w")
    users_file.write(json.dumps(simulator_obj.users))
    users_file.close()


def add_new_user(simulator_obj, user, user_filename, type):
    print("user sssss", simulator_obj.users)
    if type not in simulator_obj.users.keys():
        simulator_obj.users[type] = dict()
    if user.first_name is not "":
        simulator_obj.users[type][user.first_name] = int(user.id)
    else:
        simulator_obj.users[type][user.main_email] = int(user.id)
    save_users(simulator_obj, user_filename)


def init_users(simulator_obj, users_filename: str):
    # Init users
    print("init user", simulator_obj.users)
    if not os.path.isfile(users_filename):
        simulator_obj.current_user = simulator_obj.mammut_api.get_fixed_mammut()
        add_new_user(
            simulator_obj,
            simulator_obj.current_user,
            users_filename,
            UserType.machine.value,
        )
    else:
        load_users(simulator_obj, users_filename)


def load_rooms(simulator_obj, rooms_filename: str):
    room_file = open(rooms_filename, "r")
    simulator_obj.rooms = json.loads(room_file.read())
    room_file.close()


def save_rooms(simulator_obj, rooms_filename: str):
    rooms_file = open(rooms_filename, "w")
    print("rooms", simulator_obj.rooms)
    rooms_file.write(json.dumps(simulator_obj.rooms))
    rooms_file.close()


def add_new_room(simulator_obj, room, rooms_filename, type, extra_suffix: str = None):
    if type not in simulator_obj.rooms.keys():
        simulator_obj.rooms[type] = dict()
    if extra_suffix is None:
        simulator_obj.rooms[type][room.title] = int(room.id)
    else:
        simulator_obj.rooms[type][room.title + extra_suffix] = int(room.id)
    save_rooms(simulator_obj, rooms_filename)


def init_rooms(simulator_obj, rooms_filename: str):
    # Init users
    print("rooms load")
    if os.path.isfile(rooms_filename):
        print("rooms load")
        load_rooms(simulator_obj, rooms_filename)
        print("rooms in simulator", simulator_obj.rooms)
