from gpscript.gpscript import install
from gpscript.gpscript import lists

f = open(f"{path}/gpscript","w")
f.write('python -c "from script.script import *; $1()" $2')
f.close()
os.system(f'chmod +x {path}/gpscript')

