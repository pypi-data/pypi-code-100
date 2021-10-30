from django.db import models
from django.contrib.auth.models import Group

from slunic.utils import get_profile_model

Profile = get_profile_model()


class SlunicGroup(models.TextChoices):
    TUTOR = "Community Tutor"
    EDITOR = "Community Editor"
    MODERATOR = "Community Moderator"
    MANAGER = "Community Manager"


def init_groups():
    tutor = Group.objects.get_or_create(name=SlunicGroup.TUTOR)  # NOQA
    editor = Group.objects.get_or_create(name=SlunicGroup.EDITOR)  # NOQA
    moderator = Group.objects.get_or_create(name=SlunicGroup.MODERATOR)  # NOQA
    manager = Group.objects.get_or_create(name=SlunicGroup.MANAGER)  # NOQA


def user_in_group(user, group):
    group = user.groups.filter(name=group).first()
    return True if group else False


def is_admin(user):
    return user.is_staff or user.is_superuser


def is_tutor(user):
    return user_in_group(user, SlunicGroup.TUTOR) or is_admin(user)


def is_editor(user):
    return user_in_group(user, SlunicGroup.EDITOR) or is_admin(user)


def is_moderator(user):
    return user_in_group(user, SlunicGroup.MODERATOR) or is_admin(user)


def is_manager(user):
    return user_in_group(user, SlunicGroup.MANAGER) or is_admin(user)


def is_suspended(user):
    if user.is_authenticated and user.profile.state in (
        Profile.State.BANNED,
        Profile.State.SUSPENDED,
        Profile.State.SPAMMER,
    ):
        return True

    return False
