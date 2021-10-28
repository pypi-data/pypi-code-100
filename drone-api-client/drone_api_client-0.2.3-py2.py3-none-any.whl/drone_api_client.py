from .category import Cron, Secrets, User, Users, Repos, Template, Builds
from .session import Session


class DroneApi(Session):

    @property
    def cron(self):
        return Cron(self)

    @property
    def secrets(self):
        return Secrets(self)

    @property
    def user(self):
        return User(self)

    @property
    def users(self):
        return Users(self)

    @property
    def repos(self):
        return Repos(self)

    @property
    def templates(self):
        return Template(self)

    @property
    def builds(self):
        return Builds(self)
