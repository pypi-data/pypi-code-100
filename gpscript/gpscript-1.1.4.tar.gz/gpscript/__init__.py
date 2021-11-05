from gpscript.gpscript import install
from gpscript.gpscript import lists

base_dir = os.environ['VIRTUAL_ENV'] 
path = os.path.join(base_dir,'bin')

f = open(f"{path}/gpscript","w")
f.write('python -c "from script.script import *; $1()" $2')
f.close()
os.system(f'chmod +x {path}/gpscript')
