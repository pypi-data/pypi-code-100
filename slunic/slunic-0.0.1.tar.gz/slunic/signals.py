import logging
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

# from allauth.account.signals import user_logged_in, user_logged_out
from slunic.utils import get_profile_model

from .models import Comment, User
from .task import create_user_awards  # , send_post_notification
from .helpers import update_user_status, update_last_login
from .configs import app_configs
from slunic import helpers

logger = logging.getLogger(app_configs.LOGGER_NAME)

after_create_post = Signal()
after_create_action = Signal()

Profile = get_profile_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw, using, **kwargs):
    pref = getattr(instance, "profile", None)
    if not pref:
        Profile.objects.create(user=instance)
    instance.profile.add_watched()


# @receiver(user_logged_in)
# def update_user_stuff(sender, request, user, **kwargs):
#     # Trigger award generation.
#     create_user_awards.delay(user_id=user.id)
#     update_user_status(user=user)


# @receiver(user_logged_out)
# def update_last_login_after_logout(sender, request, user, **kwargs):
#     # Trigger award generation.
#     update_last_login(user=user)

# @receiver(after_create_post)
# def notify_post_author(sender, instance, **kwargs):
#     if instance.type in [Post.COMMENT, Post.ANSWER]:
#         # get post ancestor, then notify all author
#         linked_posts = instance.get_ancestors(ascending=False, include_self=False)
#         recipient_ids = [post.author.id for post in linked_posts]
#         verb = _("create a response")
#         notify.send(
#             instance.author,
#             recipient=instance.author,
#             verb=verb,
#             action_object=instance,
#             target=instance.parent,
#         )
#         send_post_notification.delay(
#             instance.author.id,
#             recipient_ids,
#             verb,
#             instance.id,
#             instance.parent.id,
#         )
#     else:
#         verb = _("create a %s" % instance.get_type_display())
#         notify.send(
#             instance.author,
#             recipient=instance.author,
#             verb=verb,
#             action_object=instance,
#         )
