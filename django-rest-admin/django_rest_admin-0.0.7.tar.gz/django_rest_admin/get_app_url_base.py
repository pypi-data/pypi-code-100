__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from django.urls import reverse

def get_app_url_base():
    front_path = reverse('django_rest_admin_default_list')
    if front_path[-1]=='/':
        front_path=front_path[:-1]

    pos = front_path.rfind('/')
    front_path=front_path[:pos]
    return front_path

