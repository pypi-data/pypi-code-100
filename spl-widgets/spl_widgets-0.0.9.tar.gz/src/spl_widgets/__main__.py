from sys import argv; import os
from . import gorilla_clean, stk_swx

modules_to_alias=[
    "gorilla_clean",
    "stk-swx"
]

cmd = argv[1:]

if cmd[0] == "gorilla_clean":
    gorilla_clean.main()

elif cmd[0] == "stk-swx":
    stk_swx.main()

elif cmd[0] == "setup":
    zprofile = f"{os.getenv('HOME')}/.zprofile"
    with open(zprofile,"r") as reader:
        lines = reader.readlines()

        for module in modules_to_alias:
            alias_str = f'alias {module}="python3 -m spl_widgets {module}"\n'
            for line in lines:
                if line == alias_str: break
            else: lines.append(alias_str)

    with open(zprofile, "w") as writer:
        writer.writelines(lines)

else: print("Bad command")