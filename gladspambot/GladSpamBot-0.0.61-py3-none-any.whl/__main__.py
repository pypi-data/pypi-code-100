import glob
from pathlib import Path
import logging
import sys
import re
import importlib
from telethon import events

from GladSpamBot import (
    Bot1,
    Bot2,
    Bot3,
    Bot4,
    Bot5,
    Bot6,
    Bot7,
    Bot8,
    Bot9,
    Bot10,
    Bot11,
    Bot12,
    Bot13,
    Bot14,
    Bot15,
    Bot16,
    Bot17,
    Bot18,
    Bot19,
    Bot20,
)


#logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

def load_prototype(glad_prototype):
    path = Path(f"spammerbots/prototype/{glad_prototype}.py")
    prototypes = "spammerbots.prototype.{}".format(glad_prototype)
    spec = importlib.util.spec_from_file_location(prototypes, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(glad_prototype)
    spec.loader.exec_module(load)
    sys.modules["spammerbots.prototype." + glad_prototype] = load
    print("Successfully loaded " + glad_prototype + " prototype.")

path = "spammerbots/prototype/*.py"
GLAD_MODULES = glob.glob(path)
for prototypes in GLAD_MODULES:
    with open(prototypes) as a:
        patt = Path(a.prototypes)
        glad_prototype = patt.stem
        load_prototype(glad_prototype.replace(".py", ""))



print("Deployed Spam Bots successfully!!")






if __name__ == "__main__":
    if Bot1:
        Bot1.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot2:
        Bot2.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot3:
        Bot3.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot4:
        Bot4.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot5:
        Bot5.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot6:
        Bot6.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot7:
        Bot7.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot8:
        Bot8.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot9:
        Bot9.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot10:
        Bot10.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot11:
        Bot11.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot12:
        Bot12.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot13:
        Bot13.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot14:
        Bot14.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot15:
        Bot15.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot16:
        Bot16.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot17:
        Bot17.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot18:
        Bot18.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot19:
        Bot19.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if Bot20:
        Bot20.run_until_disconnected()
    else:
        pass