import logging
import random
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import utc
from django.utils.translation import gettext_lazy as _

from .models import Page, Reaction, Badge, Award, Question, Comment, Tutorial
from .configs import app_configs

logger = logging.getLogger(app_configs.LOGGER_NAME)

User = get_user_model()


def now():
    return datetime.utcnow().replace(tzinfo=utc)


def wrap_qs(cond, klass, pk):

    return klass.objects.filter(pk=pk) if cond else klass.objects.none()


class AwardDefinition(object):
    def __init__(
        self,
        name,
        desc,
        func,
        icon,
        max=None,
        level=Badge.Level.BRONZE,
        category=Badge.Category.MISC,
        state=Badge.State.ACTIVE,
    ):
        self.name = name
        self.slug = slugify(name.lower())
        self.desc = desc
        self.fun = func
        self.icon = icon
        self.level = level
        self.category = category
        self.state = state
        self.max = max

    def get_awards(self, user):

        try:
            value = self.fun(user).order_by("pk")
            # Only return the ones that have one
        except Exception as exc:
            logger.error("validator error %s" % exc)
            return []

        if isinstance(value.first(), Page):
            # Count awards user has for this page.
            award_count = Count("award", filter=Q(author=user))

            # Get pages/user combo that have not been awarded yet
            value = value.annotate(award_count=award_count).filter(award_count=0)

            return value

        # Existing award user has won at this point.
        awarded = Award.objects.filter(badge__name=self.name, user=user)

        # Ensure users does not get over rewarded.
        if self.max and len(awarded) >= self.max:
            return []
        return value

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "desc": self.desc,
            "icon": self.icon,
            "level": self.level,
            "category": self.category,
            "state": self.state,
        }

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


AUTOBIO = AwardDefinition(
    name="Autobiographer",
    desc=_("has more than 80 characters in the information field of the user's profile"),
    func=lambda user: wrap_qs(len(user.profile.bio) > 80, User, user.id),
    max=1,
    icon="bullhorn icon",
)


CURATOR = AwardDefinition(
    name="Curator",
    desc=_("Accepted atleast once"),
    func=lambda user: wrap_qs(
        len(user.profile.bio) > 80
        and Comment.objects.filter(author=user, type=Comment.Type.ANSWER, accepted=True) > 0,
        User,
        user.id,
    ),
    max=1,
    icon="bullhorn icon",
    category=Badge.Category.ANSWER,
)


GOOD_QUESTION = AwardDefinition(
    name="Good Question",
    desc=_("Asked a question that was upvoted at least 5 times"),
    func=lambda user: Question.objects.filter(vote_count__gte=5, author=user),
    max=1,
    icon="question circle icon",
    category=Badge.Category.QUESTION,
)

GOOD_ANSWER = AwardDefinition(
    name="Good Answer",
    desc=_("Created an answer that was upvoted at least 5 times"),
    func=lambda user: Comment.objects.filter(type=Comment.Type.ANSWER, vote_count__gt=5, author=user),
    max=1,
    icon="book icon",
    category=Badge.Category.ANSWER,
)

STUDENT = AwardDefinition(
    name="Student",
    desc=_("Asked a question with at least 3 up-votes"),
    func=lambda user: Question.objects.filter(vote_count__gt=2, author=user),
    max=1,
    icon="graduation cap icon",
    category=Badge.Category.QUESTION,
)

TEACHER = AwardDefinition(
    name="Teacher",
    desc=_("Created an answer with at least 3 up-votes"),
    func=lambda user: Comment.objects.filter(type=Comment.Type.ANSWER, vote_count__gt=2, author=user),
    max=1,
    icon="smile icon",
    category=Badge.Category.ANSWER,
)

COMMENTATOR = AwardDefinition(
    name="Commentator",
    desc=_("Created a comment with at least 3 up-votes"),
    func=lambda user: Comment.objects.filter(vote_count__gt=2, author=user),
    max=1,
    icon="mycomment icon",
    category=Badge.Category.COMMENT,
)

CENTURION = AwardDefinition(
    name="Centurion",
    desc=_("Created 100 pages"),
    func=lambda user: wrap_qs(Page.objects.filter(author=user).count() > 100, User, user.id),
    max=1,
    icon="bolt icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.POST,
)

EPIC_QUESTION = AwardDefinition(
    name="Epic Question",
    desc=_("Created a question with more than 10,000 views"),
    func=lambda user: Question.objects.filter(view_count__gt=10000, author=user),
    max=1,
    icon="bullseye icon",
    level=Badge.Level.GOLD,
    category=Badge.Category.QUESTION,
)

POPULAR = AwardDefinition(
    name="Popular Question",
    desc=_("Created a question with more than 1,000 views"),
    func=lambda user: Question.objects.filter(view_count__gt=1000, author=user),
    max=1,
    icon="eye icon",
    level=Badge.Level.GOLD,
    category=Badge.Category.QUESTION,
)

ORACLE = AwardDefinition(
    name="Oracle",
    desc=_("Created more than 1,000 pages (questions + answers + comments)"),
    func=lambda user: wrap_qs(Page.objects.filter(author=user).count() > 1000, User, user.id),
    max=1,
    icon="sun icon",
    level=Badge.Level.GOLD,
    category=Badge.Category.POST,
)

PUNDIT = AwardDefinition(
    name="Pundit",
    desc=_("Created a comment with more than 10 votes"),
    func=lambda user: Comment.objects.filter(vote_count__gt=10, author=user),
    max=1,
    icon="comments icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.COMMENT,
)

GURU = AwardDefinition(
    name="Guru",
    desc=_("Received more than 100 upvotes"),
    func=lambda user: wrap_qs(
        Reaction.objects.filter(
            page__author=user,
            type=Reaction.Type.UP,
        ).count()
        > 100,
        User,
        user.id,
    ),
    max=1,
    icon="beer icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.REACTION,
)

CYLON = AwardDefinition(
    name="Cylon",
    desc=_("Received 1,000 up votes"),
    func=lambda user: wrap_qs(
        Reaction.objects.filter(
            page__author=user,
            type=Reaction.Type.UP,
        ).count()
        > 1000,
        User,
        user.id,
    ),
    max=1,
    icon="rocket icon",
    level=Badge.Level.GOLD,
    category=Badge.Category.REACTION,
)

VOTER = AwardDefinition(
    name="Voter",
    desc=_("Voted more than 100 times"),
    func=lambda user: wrap_qs(Reaction.objects.filter(user=user).count() > 100, User, user.id),
    max=1,
    icon="thumbs up outline icon",
    category=Badge.Category.REACTION,
)

SUPPORTER = AwardDefinition(
    name="Supporter",
    desc=_("Voted at least 25 times"),
    func=lambda user: wrap_qs(Reaction.objects.filter(user=user).count() > 25, User, user.id),
    max=1,
    icon="thumbs up icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.REACTION,
)

SCHOLAR = AwardDefinition(
    name="Scholar",
    desc=_("Created an answer that has been accepted"),
    func=lambda user: Comment.objects.filter(type=Comment.Type.ANSWER, author=user, accepted=True),
    max=1,
    icon="university icon",
    category=Badge.Category.ANSWER,
)

PROPHET = AwardDefinition(
    name="Prophet",
    desc=_("Created a page with more than 20 subscribers"),
    func=lambda user: Tutorial.objects.filter(author=user, subscriber_count__gt=20),
    max=1,
    icon="leaf icon",
    category=Badge.Category.TUTORIAL,
)

LIBRARIAN = AwardDefinition(
    name="Librarian",
    desc=_("Created a page with more than 10 bookmarks"),
    func=lambda user: Page.objects.filter(author=user, bookmark_count__gt=10),
    max=1,
    icon="bookmark outline icon",
    category=Badge.Category.POST,
)


def rising_star(user):
    # The user joined no more than three months ago
    cond = now() < user.date_joined + timedelta(weeks=15)
    cond = cond and Page.objects.filter(author=user).count() > 50
    return wrap_qs(cond, User, user.id)


RISING_STAR = AwardDefinition(
    name="Rising Star",
    desc=_("Created 50 pages within first three months of joining"),
    func=rising_star,
    icon="star icon",
    max=1,
    level=Badge.Level.GOLD,
    category=Badge.Category.POST,
)


GREAT_QUESTION = AwardDefinition(
    name="Great Question",
    desc="Created a question with more than 5,000 views",
    func=lambda user: Question.objects.filter(author=user, view_count__gt=5000),
    icon="fire icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.QUESTION,
)

GOLD_STANDARD = AwardDefinition(
    name="Gold Standard",
    desc=_("Created a page with more than 25 bookmarks"),
    func=lambda user: Page.objects.filter(author=user, bookmark_count__gt=25),
    icon="bookmark icon",
    level=Badge.Level.GOLD,
    category=Badge.Category.POST,
)

APPRECIATED = AwardDefinition(
    name="Appreciated",
    desc="Created a page with more than 5 votes",
    func=lambda user: Page.objects.filter(author=user, vote_count__gt=5),
    icon="heart icon",
    level=Badge.Level.SILVER,
    category=Badge.Category.POST,
)


ALL_AWARDS = [
    # These awards can only be earned once
    AUTOBIO,
    STUDENT,
    TEACHER,
    COMMENTATOR,
    SUPPORTER,
    SCHOLAR,
    VOTER,
    CENTURION,
    CYLON,
    RISING_STAR,
    GURU,
    POPULAR,
    EPIC_QUESTION,
    ORACLE,
    PUNDIT,
    GOOD_ANSWER,
    GOOD_QUESTION,
    PROPHET,
    LIBRARIAN,
    # These awards can be won multiple times
    GREAT_QUESTION,
    GOLD_STANDARD,
    APPRECIATED,
]


@transaction.atomic
def init_badges():
    for award in ALL_AWARDS:
        try:
            badge = Badge.objects.get(slug=award.slug, name=award.name)
            for key, value in award.to_dict().items():
                setattr(badge, key, value)
        except Badge.DoesNotExist as err:
            logger.info(err)
            logger.info("Creating new badge %s" % award.name)
            badge = Badge(**award.to_dict())
        badge.save()


def valid_awards(user):
    """
    Return list of valid awards for a given user
    """

    valid = []
    # Randomly go from one badge to the other
    for award in ALL_AWARDS:

        # Valid award targets the user has earned
        targets = award.get_awards(user)
        for target in targets:
            page = target if isinstance(target, Page) else None
            date = page.last_edited_at if page else user.profile.last_login
            badge = Badge.objects.filter(name=award.name).first()
            valid.append((user, badge, date or timezone.now(), page))
    return valid


def create_user_awards(user, limit=None):

    limit = limit or app_configs.USER_MAX_AWARDS_PER_SESSION

    # debugging
    # Award.objects.all().delete()

    # Collect valid targets
    valid = valid_awards(user=user)

    # Pick random awards to give to user
    random.shuffle(valid)

    valid = valid[:limit]
    awards = []
    for target in valid:
        user, badge, date, page = target
        # Set the award date to the page edit date
        date = page.last_edit_at if page else date
        # Create an award for each target.
        award = Award.objects.create(user=user, badge=badge, date=date, page=page)
        awards.append(award)
    return awards
