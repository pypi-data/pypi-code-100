import os


# windows仅支持8种颜色

os.system("")  # print颜色开启(玄学)
# 打印开关
isPrint = True


def set_isPrint(is_print=True):
    global isPrint
    isPrint = is_print


def get_isPrint():
    return isPrint


# 黑色、红色、绿色、黄色、蓝色、紫红、靛蓝、白色
_color = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "purple-red": "35",
    "cyanine": "36",
    "white": "37",
    "default": "37",
}
# 黑色、红色、绿色、黄色、蓝色、紫红、靛蓝、白色
_background = {
    "black": "40;",
    "red": "41;",
    "green": "42;",
    "yellow": "43;",
    "blue": "44;",
    "purple-red": "45;",
    "cyanine": "46;",
    "white": "47;",
    "default": "",
}
# 默认、高亮、下划线、闪烁、反白、不显示
_effect = {
    "default": "0",
    "highlight": "1",
    "underline": "4",
    "flash": "5",
    "backwhite": "7",
    "unshow": "8",
}
# 类型：简化设置
_Type = {
    "error": ["red", "underline", "default"],
    "warning": ["yellow", "default", "default"],
    "success": ["green", "default", "default"],
    "data": ["blue", "default", "default"],
    "system": ["cyanine", "default", "default"],
    "normal": ["default", "default", "default"],
}


# 打印函数（带颜色和输出控制）
def printf(
        *value,
        color="default",
        effect="default",
        background="default",
        Type=None,
        control=False,
        sep=' ',
        end='\n',
        file=None,
        flush=False
):
    if Type:
        if Type in _Type.keys():
            color = _Type[Type][0]
            effect = _Type[Type][1]
            background = _Type[Type][2]
        else:
            print("\033[31m颜色类型参数错误\033[0m")
            color = "default"
            effect = "default"
            background = "default"
    else:
        if color not in _color.keys():
            print("\033[31m打印函数字体颜色参数错误\033[0m")
            color = "default"
        if effect not in _effect.keys():
            print("\033[31m打印函数显示方式参数错误\033[0m")
            effect = "default"
        if background not in _background.keys():
            print("\033[31m打印函数背景色参数错误\033[0m")
            background = "default"
    if isPrint or control:
        print("\033[%s;%s%sm" % (_effect[effect], _background[background], _color[color]), sep="", end="")
        print(*value, sep=sep, end="\033[0m" + end, file=file, flush=flush)


if __name__ == '__main__':
    printf("thgttr", "sdsdds", Type="error")
    printf("ssdd", Type="system")
