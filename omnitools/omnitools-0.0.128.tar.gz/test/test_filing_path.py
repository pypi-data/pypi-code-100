from omnitools import *


try:
    print(temp_dir())
except:
    print("no temp dir")
print(abs_main_dir())
print(abs_dir(__file__))
print(join_path(abs_dir(__file__), "..", "test555"))
print(get_cwd())

