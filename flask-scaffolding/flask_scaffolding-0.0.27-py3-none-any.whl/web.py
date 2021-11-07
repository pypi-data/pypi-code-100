import os 
import sys
import shutil
import time 

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
    print("\n[INFO] Prepare to create a new Flask Scaffoling Base with name %s in path %s" % (app_name, app_dir))
    time.sleep(2)

    # check
    app_path = os.path.join(app_dir, app_name)
    app_path_exist = os.path.exists(app_path)
    base_path_valid = os.path.exists(app_dir)

    print("\n[INFO] Checking for full path %s" % app_path)
    time.sleep(2)
    if not app_path_exist and base_path_valid : 
        os.mkdir(app_path)
        try : 
            pkgdir = sys.modules['scaffold'].__path__[0]
            source_path = os.path.join(pkgdir, 'base')
            copytree(source_path, app_path)
            print("\n[INFO] Generating Flask Scaffoling Base Completed!")
            print("\n[INFO] Before invoking app, please setup Flask-Mail configuration in instance/config.py \n"\
            "MAIL_SERVER= \n"\
            "MAIL_PORT= \n"\
            "MAIL_USE_SSL= \n"\
            "MAIL_USERNAME= \n"\
            "MAIL_PASSWORD= \n")
            print("\n[INFO] Invoking app by running run.py")
            print("\n[INFO] Default User : \n john@mail.com / john123")

        except  Exception as e:
            print("[ERROR]", e) 
    else : 
        if app_path_exist :
            print("[ERROR] Cannot creating app directory path %s exist." % app_path) 
        if not base_path_valid :  
            print("[ERROR] Cannot creating base directory path %s not found." % app_dir) 
