import os

def clear():  # ¤ Clears os
    os.system("cls" if os.name == "nt" else "clear")