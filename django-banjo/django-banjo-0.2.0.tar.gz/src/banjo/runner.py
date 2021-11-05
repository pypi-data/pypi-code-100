import os
from os.path import abspath, dirname, join
import sys
import django
import shutil
from pathlib import Path
from subprocess import run
from django.conf import settings
from django.core import management

sys.path.insert(0, '.')

def setup_django(debug=False):
    if debug:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings_debug')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings')
    django.setup()

    # Loading views causes banjo's route_get and route_post decorators to be invoked,
    # which populates banjo.urls:urlpatterns. 
    from app import views

    management.execute_from_command_line(['', 'makemigrations', 'app', 'banjo'])
    management.execute_from_command_line(['', 'migrate'])

def init_heroku():
    print("Checking configuration for Heroku deployment...")
    print(" * Checking for app/ folder") 
    app_path = Path('app')
    if not app_path.is_dir():
        raise OSError("Missing a directory called 'app'")
    print(" * Checking for heroku executable")
    if shutil.which('heroku') is None:
        raise OSError("Heroku is not installed.")
    print(" * Checking that django-banjo is installed")
    import banjo
    print(" * Checking that gunicorn is installed")
    import gunicorn
    print(" * Checking that django-heroku is installed")
    import django_heroku
    print(" * Checking for requirements.txt")
    if not Path('requirements.txt').exists():
        with open('requirements.txt', 'w') as fh:
            fh.write(run(['pip', 'freeze'], capture_output=True, text=True).stdout)
        print(" --> Created requirements.txt")
    print(" * Checking for wsgi.py")
    if not Path("wsgi.py").exists():
        with open('wsgi.py', 'w') as fh:
            fh.write('\n'.join([
                "import os",
                "from django.core.wsgi import get_wsgi_application",
                "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings_heroku')",
                "application = get_wsgi_application()",
                "from app import views",
            ]))
        print(" --> Created wsgi.py")
    print(" * Checking for Procfile")
    if not Path('Procfile').exists():
        with open('Procfile', 'w') as fh:
            fh.write('web: gunicorn wsgi')
        print(" --> Created Procfile")

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-s", "--shell", action="store_true")
    parser.add_argument("-i", "--init_heroku", action="store_true")
    parser.add_argument("-p", "--port", type=int, default=5000)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if args.shell:
        setup_django(args.debug)
        management.execute_from_command_line(['', 'shell_plus'])
    elif args.init_heroku:
        init_heroku()
    else:
        setup_django(args.debug)
        management.execute_from_command_line(['', 'runserver', str(args.port)])
