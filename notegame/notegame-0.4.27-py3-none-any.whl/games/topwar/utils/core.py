

field_list = {
    "id": "id",
    "pid": "pid",
    "nickname": "nick_name",
    "username": "user_name",
    "nationalflag": "national_flag",
    "usergender": "user_gender",
    "gender": "gender",
    "avatarurl": "avatar_url",
    "headimgurl": "head_img_url",
    "power": "power",
    "level": "player_level",
    "shieldTime": "shield_time",
    "fireTime": "fire_time",
    "province": "province",
    "x": "x",
    "y": "y",
    "k": "k",
    "aid": "aid",
    "a_tag": "a_tag",
    "pointType": "point_type",
    "ownerId": "owner_id",
    "itemId": "item_id",
    "expireTime": "expire_time"
}


def merge_info(update_dict: dict, properties: dict = None):
    properties = properties or {}
    for key, value in field_list.items():
        if key in update_dict.keys():
            properties[value] = update_dict[key]
    return properties


def spiral_traverse(end_row=10, end_col=10, start_row=0, start_col=0, step=1, reverse=True):
    result = []
    while start_row <= end_row and start_col <= end_col:
        result.extend([[start_row, col] for col in range(start_col, end_col, step)])
        result.extend([[row, end_col] for row in range(start_row, end_row, step)])
        result.extend([[end_row, col] for col in range(end_col, start_col, -2)])
        result.extend([[row, start_col] for row in range(end_row, start_row, -2)])
        start_row += step
        end_row -= step
        start_col += step
        end_col -= step
    if reverse:
        result = result[::-1]
    return result
