from sys import argv; import os
from . import gorilla_clean, stk_swx, widget_help

modules_to_alias=[
    "update_widgets",
    "help",
    "gorilla_clean",
    "stk-swx"
]

cmd = argv[1:]

if cmd[0] == "gorilla_clean":
    gorilla_clean.main()

elif cmd[0] == "stk-swx":
    stk_swx.main()

elif cmd[0] == "help":
    widget_help.main()

elif cmd[0] == "update_widgets":
    os.system("pip install spl_widgets --upgrade")
    zprofile = f"{os.getenv('HOME')}/.zprofile"
    with open(zprofile,"r") as reader:
        lines = reader.readlines()

        for module in modules_to_alias:
            alias_str = f'alias {module}="python3 -m spl_widgets {module}"\n'
            for line in lines:
                if line == alias_str: break
                elif "spl_widgets" in line and not any([module in line for module in modules_to_alias]):
                    print(f"Removed old alias: {line[:-1]}")
                    line="KILL"+line
            else: lines.append(alias_str)

    with open(zprofile, "w") as writer:
        writer.writelines([line for line in lines if not line.startswith("KILL")])

else: print("Bad command")