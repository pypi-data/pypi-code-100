import sys
import os

def setup_django(settings_file):
    try:
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)
        django.setup()
        exit(0)
    except Exception: 
        exit(-1)


if __name__=="__main__":
    setup_django(sys.argv[1])

