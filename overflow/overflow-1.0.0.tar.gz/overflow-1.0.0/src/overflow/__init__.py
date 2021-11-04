print("non-functional version")
import subprocess,platform
s = input("do you want an update? Y/N \n")
if s.upper() == "Y":
	if platform.system() == "Windows":
		print(subprocess.run("py -m pip install -U overflow"))
	else:
		print(subprocess.run("python3 -m pip install -U overflow"))
else:
	exit()