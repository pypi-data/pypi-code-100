import random
from django_rq import job
from django.utils.translation import gettext_lazy as _
# from notifications.signals import notify
from slunic.configs import app_configs


def message(msg, level=0):
    print(f"{msg}")


@job
def create_user_awards(user_id, limit=None):
    from slunic.models import User, Award
    from slunic.helpers import valid_awards, get_bot_user

    limit = limit or app_configs.MAX_AWARDS_PER_SESSION

    bot = get_bot_user()
    user = User.objects.filter(id=user_id).first()
    # debugging
    # Award.objects.all().delete()

    # Collect valid targets
    valid = valid_awards(user=user)

    # Pick random awards to give to user
    random.shuffle(valid)

    valid = valid[:limit]

    for target in valid:
        user, badge, date, post = target
        # Set the award date to the post edit date
        date = post.lastedit_date if post else date
        # Create an award for each target.
        award = Award.objects.create(user=user, badge=badge, date=date, post=post)
        # Notify user
        # notify.send(bot, recipient=user, verb=_("earn award"), action_object=award)


@job
def send_post_notification(sender_id, recipient_ids, verb, action_object_id=None, target_id=None, **kwargs):
    """Send notification task"""
    from slunic.models import Post
    from django.contrib.auth import get_user_model
    # from notifications.signals import notify

    User = get_user_model()
    sender = User.objects.get(pk=sender_id)
    recipients = User.objects.filter(pk__in=recipient_ids)
    data = {
        "sender": sender,
        "verb": verb,
    }
    if action_object_id:
        action_object = Post.objects.get(pk=action_object_id)
        data.update({"action_object": action_object})
    if target_id:
        target = Post.objects.get(pk=target_id)
        data.update({"target": target})

    for recipient in recipients:
        data.update({"recipient": recipient})
        # notify.send(**data)


@job
def send_notification(sender, recipient, verb, action_object=None, target=None, description=None, **kwargs):
    # notify.send(
    #     sender,
    #     recipient=recipient,
    #     verb=verb,
    #     action_object=action_object,
    #     target=target,
    #     description=description
    # )
    pass
