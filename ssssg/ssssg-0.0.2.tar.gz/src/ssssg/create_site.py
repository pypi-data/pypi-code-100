from .site_creator import JinjaSiteCreator


def create_site():
    j = JinjaSiteCreator()
    j.create_site()
    j.start_dev_server()
