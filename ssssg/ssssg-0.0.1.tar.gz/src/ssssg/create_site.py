from .site_creator import JinjaSiteCreator


if __name__ == "__main__":
    j = JinjaSiteCreator()
    j.create_site()
    j.start_dev_server()
