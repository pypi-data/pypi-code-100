import os
import requests
import sys

print("Welcome to gpscript...")


a = requests.get('https://raw.githubusercontent.com/ujjwalkar0/General-Purpose-Scripts/main/packages.json')

def lists():
    for i in a.json():
        print(i)

def installed():
    print("Loading Installed Scripts...")
    base_dir = os.environ['VIRTUAL_ENV'] 
    path = os.path.join(base_dir,'applications')
    j=0
    for i in os.listdir(path):
        j+=1
        print(f'{j}. {i}'.lower().replace('_',''))

def install():
    if 'VIRTUAL_ENV' not in os.environ:
        print( "Don't do this without virtual environment.")
        return
    
    arg = sys.argv[1]
    dj = dict(a.json())

    try:
        app = dj[arg]
        print(app)
    except KeyError:
        print( "error: Target not found, program does not exist or not in package.json :",arg)
        return

    base_dir = os.environ['VIRTUAL_ENV'] 
    path = os.path.join(base_dir,'applications')
    installdir = os.path.join(path,arg.replace('_',' '))

    try:
        os.mkdir(installdir)
    except FileNotFoundError:
        os.mkdir(path)
        os.mkdir(installdir)
    except FileExistsError:
        pass
        print("App already installed")
        return   
    print('Connecting to server...')
    url = 'https://github.com/ujjwalkar0/General-Purpose-Scripts/trunk/scripts/'+arg.replace(' ','%20')
    
    print('Connected...')

    print('Downloading',arg+'...')
    installdir = installdir.replace(' ','\ ')
    appname = arg.lower().replace('_','')
    os.system(f'echo "python {installdir}/{app}" > {base_dir}/bin/{appname} && chmod +x {base_dir}/bin/{appname} ')

    os.system(f'svn checkout {url} {installdir}')
    print("Installing requirements...")
    os.system(f'pip install -r {installdir}/requirements.txt')


def path(appname):
    base_dir = os.environ['VIRTUAL_ENV'] 
    apppath = os.path.join(base_dir,'bin',appname)
    appdirct = '/'
    f = open(apppath,'r+')
    a = f.read().split('/')
    print(a)
    i = 0
    while(a[i-1] != 'applications'):
        i+=1
        appdirct = os.path.join(appdirct,a[i])

    f.close()
    return apppath,appdirct

def update():
    arg = sys.argv[1]
    apppath,appdir = path(arg)
    os.system(f'svn update {appdir}')

def remove():
    arg = sys.argv[1]
    apppath,appdir = path(arg)

    if not os.path.exists(apppath):
        print(apppath,"Program Not exist")
        return
    
    if not os.path.exists(appdir):
        print(appdir,"Program Directory Not exist")
        return
    
    os.system(f'rm {apppath} && rm -rf {appdir}')