from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...awards import create_user_awards

User = get_user_model()


class Command(BaseCommand):
    help = "Init Badges"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            awards = create_user_awards(user)
            if awards:
                awards_text = ",".join([str(a) for a in awards])
                self.stdout.write("%s successfully earned [%s]" % (user, awards_text))
            else:
                self.stdout.write("%s require more activity." % user)
