import os 
import sys
import shutil

# utils
def get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)



if __name__ == '__main__':
    # read parameter 
    app_name = get(sys.argv, 1, default='app') 
    app_dir = get(sys.argv, 2, default=os.getcwd()) 

    # check
    app_path = os.path.join(app_dir, app_name)
    app_path_exist = os.path.exists(app_path)
    base_path_valid = os.path.exists(app_dir)

    if not app_path_exist and base_path_valid : 
        os.mkdir(app_path)
        try : 
            pkgdir = sys.modules['scaffold'].__path__[0]
            source_path = os.path.join(pkgdir, 'base')
            copytree(source_path, app_path)
            print("[INFO] Generating Flask Scaffoling Base Completed!")
        except  Exception as e:
            print("[ERROR]", e) 
    else : 
        if app_path_exist :
            print("[ERROR] cannot creating app directory path %s exist." % app_path) 
        if not base_path_valid :  
            print("[ERROR] cannot creating base directory path %s not found." % app_dir) 
