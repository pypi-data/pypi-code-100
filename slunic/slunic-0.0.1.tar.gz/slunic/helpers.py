import re
import os
import json
import logging
from datetime import timedelta
from difflib import SequenceMatcher, unified_diff

from django.db import NotSupportedError, transaction
from django.db.models import F
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model

from slunic import utils, models, configs

app_configs = configs.app_configs
logger = logging.getLogger(app_configs.LOGGER_NAME)
User = get_user_model()
Profile = utils.get_profile_model()


def get_bot_user():
    bot_user = User.objects.get(username=app_configs.BOT_USERNAME)
    return bot_user


def update_user_status(user):
    # Update a new user into trusted after a threshold score is reached.
    if (user.profile.state == Profile.State.NEW) and (user.profile.score > 50):
        user.profile.state = Profile.State.TRUSTED
        user.save()
        return True
    return user.profile.trusted


def recreate_user_profile():
    for user in User.objects.all():
        profile = getattr(user, "profile", None)
        if not profile:
            profile = Profile(user=user)
            profile.save()


def update_last_login(user):
    user.profile.last_login = timezone.now()
    user.save()
    return user.profile


def diff_ratio(text1, text2):
    # Do not match on spaces
    s = SequenceMatcher(lambda char: re.match(r"\w+", char), text1, text2)
    return round(s.ratio(), 5)


def get_traffic(days=1):
    """
    Obtains the number of distinct IP numbers.
    """
    recent = timezone.now() - timedelta(days=days)
    try:
        traffic = models.Visitor.objects.filter(date__gt=recent).distinct("ip").count()
    except NotSupportedError:
        traffic = models.Visitor.objects.filter(date__gt=recent).values_list("ip")
        traffic = [t[0] for t in traffic]
        traffic = len(set(traffic))
    # It is possible to not have hit any postview yet.
    traffic = traffic or 1
    return traffic


def update_page_views(page, request):
    """
    Views are updated per interval.
    """

    # Get the ip.
    ip = utils.get_ip(request)

    # Keys go by IP and post ip.
    cache_key = app_configs.CACHE_PAGE_VIEW_KEY % {"page_id": page.id, "ip": ip}
    timeout = app_configs.CACHE_PAGE_VIEW_TIMEOUT

    # Found hit no need to increment the views
    if cache.get(cache_key):
        return

    # Insert a new view into database.
    models.Visitor.objects.create(ip=ip, page=page)

    # Separately increment post view.
    page.view_count += 1
    page.save()

    # Set the cache.
    cache.set(cache_key, 1, timeout)

    # Drop the post related cache for logged in users.
    if request.user.is_authenticated:
        utils.delete_page_cache(page)

    return page


def stat_file(date, data=None, load=False, dump=False):

    os.makedirs(app_configs.STATS_DIR, exist_ok=True)
    file_name = f"{date.year}-{date.month}-{date.day}.json"
    file_path = os.path.normpath(os.path.join(app_configs.STATS_DIR, file_name))

    def load_file():
        # This will be FileNotFoundError in Python3.
        if not os.path.isfile(file_path):
            raise IOError
        with open(file_path, "r") as fin:
            return json.loads(fin.read())

    def dump_into_file():
        with open(file_path, "w") as fout:
            fout.write(json.dumps(data))

    if load:
        return load_file()

    if dump:
        return dump_into_file()


def compute_stats(start, end):
    User = get_user_model()
    users_total = User.objects.count()
    users_active = User.objects.filter(is_active=True).count()
    # Get Posts States

    # tutorials_count = Tutorial.objects.only("pk").filter(created_at__lt=end).count()
    # questions_count = Question.objects.only("pk").filter(created_at__lt=end).count()
    # comments_count = Comment.objects.only("pk").filter(type=Post.COMMENT, created_at__lt=end).count()
    # answers_count = Answer.objects.only("pk").filter(type=Post.ANSWER, created_at__lt=end).count()
    votes_count = models.Reaction.objects.filter(date__lt=end).count()

    new_users = User.objects.filter(
        date_joined__gte=start,
        date_joined__lt=end,
    ).values_list("id", flat=True)

    # new_posts = Post.objects.filter(
    #     created_at__gte=start,
    #     created_at__lt=end,
    # ).values_list("uid", flat=True)

    new_votes = models.Reaction.objects.filter(
        date__gte=start,
        date__lt=end,
    ).values_list("uid", flat=True)

    slunic_states = {
        "date": utils.datetime_to_iso(start),
        "timestamp": utils.datetime_to_unix(start),
        "users_total": users_total,
        "users_active": users_active,
        "votes_count": votes_count,
        "new_users": new_users,
        # "new_posts": new_posts,
        "new_votes": new_votes,
        "new_traffic": get_traffic(),
    }
    return slunic_states


def get_slunic_stats(date=None):
    """
    Statistics about this website for the given date.
    Statistics are stored to a json file for caching purpose.
    Parameters:

    date -- a `datetime`.

    """

    start = timezone.now() if not date else date
    end = start + timedelta(days=1)
    cache_key = app_configs.CACHE_APP_STATS_KEY % {"timestamp": utils.datetime_to_unix(end)}
    timeout = app_configs.CACHE_APP_STATS_TIMEOUT

    slunic_states = cache.get(cache_key)
    if not slunic_states:
        # try:
        #     slunic_states = stat_file(date=start, load=True)
        # except Exception:  # This will be FileNotFoundError in Python3.
        #     logger.info("No stats file for {}.".format(start))
        data = {}
        data.update(compute_stats(start=start, end=end))

        # if not settings.DEBUG:
        # stat_file(dump=True, date=start, data=data)
        cache.set(cache_key, data, timeout)
    return slunic_states


def get_user_stats(user):
    Reaction = models.Reaction

    cache_key = app_configs.CACHE_USER_STATS_KEY % {"user_id": user.id}
    timeout = app_configs.CACHE_USER_STATS_TIMEOUT
    user_states = cache.get(cache_key)

    if not user_states:
        # Get Tutorials States

        # views_count = user.posts.filter(type__in=Post.TOP_LEVEL).aggregate(total_views=Sum("view_count"))
        # spam_count = Post.objects.filter(is_spam=True).count()
        reaction_count = Reaction.objects.filter(post__author=user).exclude(user=user).count()
        # Recent
        # created_at = {"created_at__gte": user.profile.last_login}
        date = {"date__gte": user.profile.last_login}
        # recent_spam_count = Post.objects.filter(is_spam=True, **created_at)[:1000].count()
        recent_reaction_count = (
            Reaction.objects.filter(page__author=user, **date).exclude(user=user)[:1000].count()
        )
        user_states = {
            # "views_count": views_count["total_views"],
            # "spam_count": spam_count,
            "reaction_count": reaction_count,
            # recent
            # "recent_spam_count": recent_spam_count,
            "recent_reaction_count": recent_reaction_count,
        }
        cache.set(cache_key, user_states, timeout)
    return user_states


@transaction.atomic
def handle_comment(user, parent, content, is_spam=False, instance=None):
    if instance is None:
        # Create comment
        instance = models.Comment(
            author=user,
            parent=parent,
            content=content,
            is_spam=is_spam,
        )
        instance.save()
        change = 1
        logger_data = dict(
            user=user,
            action=models.Log.CREATE,
            text="create comment",
            target=None,
            page=instance,
        )
    elif isinstance(instance, models.Comment):
        # Update comment
        instance.parent = parent
        instance.content = content
        instance.edited_by = user
        instance.is_spam = is_spam
        instance.save()
        logger_data = dict(
            user=user,
            action=models.Log.CREATE,
            text="edit comment",
            target=None,
            page=instance,
        )
    else:
        raise ValueError("instance must be Comment instance")
    ancestors = instance.get_ancestors(include_self=False)
    # Update reply count on anchestors
    ancestors.update(comment_count=F("comment_count") + change)
    recipients = [p.author for p in ancestors]
    print("Create page log. %s " % logger_data)
    print("sending notification  %s to question or tutorial." % recipients)

    # remove (Tutorial, Qustion) page cache
    utils.delete_page_cache(instance.get_root())

    return instance


def db_logger(user=None, action=models.Log.MODERATE, text="", target=None, ipaddr=None, post=None):
    """
    Creates a database log.
    """
    models.Log.objects.create(user=user, action=action, text=text, target=target, ipaddr=ipaddr, post=post)
    logger.info(f"user={user.email} {text} ")


def handle_diff(text, page, user):
    """
    Compute and return Diff object for diff between text and post.content
    """

    # Skip on post creation
    if not page:
        return

    ratio = diff_ratio(text1=text, text2=page.content)

    # Skip no changes detected
    if ratio == 1:
        return

    # Compute diff between text and post.
    content = page.content.splitlines()
    text = text.splitlines()

    diff = unified_diff(content, text)
    diff = [f"{line}\n" if not line.endswith("\n") else line for line in diff]
    diff = "".join(diff)

    # See if a diff has been made by this user in the past 10 minutes
    dobj = models.Diff.objects.filter(page=page, author=page.author).first()

    # 10 minute time frame between
    frame = 60 * 10
    delta = (timezone.now() - dobj.created).seconds if dobj else frame

    # Create diff object within time frame or the person editing is a mod.
    if delta >= frame or user != page.author:
        # Create diff object for this user.
        dobj = models.Diff.objects.create(diff=diff, page=page, original=page.content, author=user)
        page.has_diff = True
        page.save()

        # Only log when anyone but the author commits changes.
        if user != page.author:
            db_logger(
                user=user,
                action=models.Log.EDIT,
                text="edited post",
                target=page.author,
                post=page,
            )

    return dobj


@transaction.atomic
def handle_vote(page, user, reaction_type):
    Reaction = models.Reaction
    Page = models.Page

    reaction = Reaction.objects.filter(user=user, page=page, type=reaction_type).first()

    if reaction:
        msg = f"{reaction.get_type_display().title()} removed"
        change = -1
        reaction.delete()
    else:
        change = +1
        reaction = Reaction.objects.create(user=user, page=page, type=reaction_type)
        msg = f"{reaction.get_type_display().title()} added"

    # Fetch update the post author score.
    if not page.author == user:
        Profile.objects.filter(user=page.author).update(score=F("score") + change)

    # Calculate counts for the current post
    reactions = list(Reaction.objects.filter(page=page))
    upvote_count = len(list(filter(lambda v: v.type == Reaction.Type.UP, reactions)))
    downvote_count = len(list(filter(lambda v: v.type == Reaction.Type.DOWN, reactions)))
    vote_count = upvote_count - downvote_count
    book_count = len(list(filter(lambda v: v.type == Reaction.Type.BOOKMARK, reactions)))
    accept_count = len(list(filter(lambda v: v.type == Reaction.Type.ACCEPT, reactions)))

    # Increment the post vote count.
    Page.objects.filter(uid=page.uid).update(vote_count=vote_count)

    # The thread vote count represents all votes in a thread
    Page.objects.filter(uid=page.get_root().uid).update(thread_votecount=F("thread_votecount") + change)

    # Increment the bookmark count.
    if reaction_type == Reaction.Type.BOOKMARK:
        Page.objects.filter(uid=page.uid).update(book_count=book_count)
        # Reset bookmark cache
        utils.delete_cache(app_configs.CACHE_USER_BOOKMARKS_KEY, user)

    # Handle accepted reaction.
    if reaction_type == Reaction.Type.ACCEPT:
        Page.objects.filter(uid=page.uid).update(accept_count=accept_count)
        Page.objects.filter(uid=page.get_root().uid).update(accept_count=F("accept_count") + change)

    page.refresh_from_db()
    utils.delete_page_cache(page)
    return msg, page, change
