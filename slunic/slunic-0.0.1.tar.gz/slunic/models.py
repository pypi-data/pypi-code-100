from functools import cached_property
import logging
from django.db import models
from django.db.models.enums import IntegerChoices
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse

from taggit.utils import parse_tags
from taggit.models import TagBase, TaggedItemBase, GenericTaggedItemBase
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from slunic.managers import TagManager, CategoryManager, ReactionManager, TutorialManager

from .configs import app_configs
from . import utils

MIN_CHARS = 20
MAX_UID = 10
MAX_TEXT = 200
MAX_CONTENT = 15000
MIN_CONTENT = 5
MAX_TITLE = 400
MAX_TAGS = 5
MAX_TAGS_TEXT = 200

User = get_user_model()
logger = logging.getLogger(app_configs.LOGGER_NAME)


class Tag(TagBase):
    name = models.SlugField(max_length=50)
    description = models.TextField(null=True, blank=True)

    objects = TagManager()

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str(self.name).lower()
        return super().save(*args, **kwargs)


class TaggedItem(GenericTaggedItemBase, TaggedItemBase):
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("tagged item")
        verbose_name_plural = _("tagged items")
        index_together = [["content_type", "object_id"]]
        unique_together = [["content_type", "object_id", "tag"]]


class Category(MPTTModel):

    uid = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            "Categories, unlike tags, category can have a hierarchy. You might have a "
            "Jazz category, and under that have children categories for Bebop"
            " and Big Band. Totally optional."
        ),
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(3),
        ],
        verbose_name=_("Category Name"),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )
    objects = CategoryManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        index_together = [["parent", "slug"]]
        unique_together = [["parent", "slug"]]

    @property
    def opts(self):
        return self._meta

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_uid(8)
        if not self.slug:
            utils.unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class Page(MPTTModel):
    class State(models.IntegerChoices):
        OPEN = 1, _("open")
        OFFTOPIC = 2, _("off topic")
        DUPLICATE = 3, _("duplicate")
        SOLVED = 4, _("solved")
        CLOSED = 5, _("closed")

    state = models.IntegerField(
        default=State.OPEN,
        choices=State.choices,
        db_index=True,
    )

    author = models.ForeignKey(
        User,
        related_name="pages",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
    )
    parent = TreeForeignKey(
        "self",
        related_name="children",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_(
            "Page, can have a hierarchy. You might have a "
            "Index, and under that have children page for Blog "
            "and Comment. Totally optional."
        ),
    )
    uid = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        editable=False,
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
        db_index=True,
    )
    title = models.CharField(max_length=240)
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("Page content."),
    )
    seo_title = models.CharField(max_length=240)
    seo_description = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
    )
    last_edited_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=True,
    )
    edited_by = models.ForeignKey(
        User,
        related_name="last_edited_posts",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("edited by"),
    )
    is_live = models.BooleanField(default=True)
    login_required = models.BooleanField(
        _("login required"),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    template_name = models.CharField(
        _("template name"),
        max_length=70,
        null=True,
        blank=True,
        help_text=_(
            "Example: “pages/contact_page.html”. If this isn’t provided, "
            "the system will use “pages/default.html”."
        ),
    )
    real_model = models.CharField(max_length=120, editable=False)

    # Indicates whether the post has accepted answer.
    answer_count = models.IntegerField(default=0, blank=True, db_index=True)

    # The number of accepted answers.
    accept_count = models.IntegerField(default=0, blank=True)

    # The number of replies for  thread.
    reply_count = models.IntegerField(default=0, blank=True, db_index=True)

    # The number of comments that a post has.
    comment_count = models.IntegerField(default=0, blank=True)

    # Number of upvotes for the post
    vote_count = models.IntegerField(default=0, blank=True, db_index=True)

    # The total numbers of votes for a top-level post.
    thread_votecount = models.IntegerField(default=0, db_index=True)

    # The number of views for the post.
    view_count = models.IntegerField(default=0, blank=True, db_index=True)

    # Bookmark count.
    book_count = models.IntegerField(default=0)

    # How many people follow that thread.
    subs_count = models.IntegerField(default=0)

    # How many people this post as spam.
    spam_count = models.IntegerField(default=0)

    has_diff = models.BooleanField(_("diff status"), default=False)

    comment_enabled = models.BooleanField(_("allow comments"), default=True)

    allowed_parents = "__all__"

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")
        index_together = [["parent", "slug"]]

    def __str__(self):
        return str(self.title)

    @property
    def opts(self):
        return self._meta

    @property
    def is_open(self):
        return self.state == Question.State.OPEN

    @property
    def is_offtopic(self):
        return self.state == Question.State.OFFTOPIC

    @property
    def is_duplicate(self):
        return self.state == Question.State.DUPLICATE

    @property
    def is_solved(self):
        return self.state == Question.State.SOLVED

    @property
    def is_closed(self):
        return self.state == Question.State.CLOSED

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError({"parent": _("Parent page cannot be self.")})
            if parent.parent and parent.parent == self:
                raise ValidationError({"parent": _("Cannot have circular Parents.")})
                # TODO ValidationError("Parent type is not allowed.")

    def get_reactions(self, user):
        return self.reactions.filter(user=user).values("type")

    def get_reaction_states(self, user, detail=True):
        """Calculate current user per request"""
        reactions = self.get_reactions(user)
        reaction_list = [act["type"] for act in reactions]
        if detail:
            states = [
                {
                    "value": tp.value,
                    "label": tp.label,
                    "state": tp.value in reaction_list,
                }
                for tp in Reaction.Type
            ]
        else:
            states = {tp.value: tp.value in reaction_list for tp in Reaction.Type}
        return states

    @property
    def comment_allowed(self):
        return (
            self.comment_enabled
            and self.level < app_configs.COMMENT_MAX_LEVEL
            and not self.is_closed
            and not self.is_solved
        )

    def get_real_model(self):
        return "%s" % self.opts.model_name

    def get_real_model_class(self, app_label="slunic"):
        """
        Return the real Model class related to objects.
        """
        model_name = "%s.%s" % (app_label, self.real_model.title())
        try:
            return apps.get_model(model_name, require_ready=False)
        except LookupError:
            raise ImproperlyConfigured(
                "real model refers to model '%s' that has not been installed" % model_name
            )

    def get_real_instance(self):
        """Return the real page instance."""
        model = self.get_real_model_class()
        instance = model.objects.get(pk=self.id)
        return instance

    def get_absolute_url(self):
        return reverse(
            "slunic_page_detail",
            kwargs={
                "model_name": self.opts.model_name,
                "id": self.id,
                "slug": self.slug,
            },
        )

    def get_root(self):
        root = super().get_root()
        instance = root.get_real_instance()
        return instance

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_uid(8)
        if not self.slug:
            utils.unique_slugify(self, self.title)
        if not self.real_model:
            self.real_model = self.get_real_model()
        return super().save(*args, **kwargs)


class Help(Page):
    summary = models.TextField(
        max_length=250,
        verbose_name=_("summary"),
        null=True,
        blank=True,
        db_index=True,
    )
    category = TreeForeignKey(
        Category,
        null=True,
        blank=True,
        related_name="help_pages",
        on_delete=models.CASCADE,
        verbose_name=_("category"),
    )

    class Meta:
        verbose_name = _("help")
        verbose_name_plural = _("helps")

    def save(self, *args, **kwargs):
        self.comment_enabled = False
        return super().save(*args, **kwargs)


class Tutorial(Page):

    summary = models.TextField(
        max_length=250,
        verbose_name=_("summary"),
        null=True,
        blank=True,
        db_index=True,
    )
    category = TreeForeignKey(
        Category,
        null=True,
        blank=True,
        related_name="tutorials",
        on_delete=models.CASCADE,
        verbose_name=_("category"),
    )
    tags = TaggableManager(
        verbose_name=_("tags"),
        through=TaggedItem,
        blank=True,
    )

    objects = TutorialManager()

    class Meta:
        verbose_name = _("tutorial")
        verbose_name_plural = _("tutorials")


class Question(Page):

    tags = TaggableManager(
        verbose_name=_("tags"),
        through=TaggedItem,
        blank=True,
    )

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


class Comment(Page):

    is_spam = models.BooleanField(default=False)

    class Type(models.IntegerChoices):
        COMMENT = 0, _("comment")
        ANSWER = 1, _("answer")

    type = models.IntegerField(default=Type.COMMENT, choices=Type.choices)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def clean(self):
        if not self.parent.comment_allowed:
            raise ValidationError({"parent": "Comment no allowed."})
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_uid(8)
        if not self.title:
            self.title = "Comment #%s %s" % (self.uid, self.parent.title)
        if not self.slug:
            utils.unique_slugify(self, self.title)
        self.real_model = self.get_real_model()
        return super().save(*args, **kwargs)


class Diff(models.Model):

    diff = models.TextField(
        default="",
        help_text=_("Initial content state"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date this change was made"),
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        help_text=_("Page, This diff belongs to"),
    )
    original = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("original page content before edited."),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_("Person who created the diff"),
    )

    def save(self, *args, **kwargs):
        self.created = self.created or timezone.now()
        super(Diff, self).save(*args, **kwargs)

    @property
    def breakline(self):
        diff = self.diff
        diff = diff.replace("\n", "<br>")
        return diff


class Badge(models.Model):
    class Level(models.IntegerChoices):
        BRONZE = 1, _("bronze")
        SILVER = 2, _("silver")
        GOLD = 3, _("gold")

    class Category(models.IntegerChoices):
        MISC = 0, _("misc")
        POST = 1, _("post")
        TUTORIAL = 2, _("tutorial")
        QUESTION = 3, _("question")
        ANSWER = 4, _("answer")
        COMMENT = 5, _("comment")
        REACTION = 6, _("reaction")

        __empty__ = _("(unknown)")

    class State(models.IntegerChoices):
        RETIRED = 0, _("retired")
        ACTIVE = 1, _("active")

    uid = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=50,
        help_text=_("The name of the badge."),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
    )
    desc = models.CharField(
        max_length=200,
        default="",
        help_text=_("The description of the badge."),
    )
    level = models.IntegerField(
        choices=Level.choices,
        default=Level.BRONZE,
        help_text=_("The rarity level of the badge."),
    )
    category = models.IntegerField(
        choices=Category.choices,
        default=Category.MISC,
        help_text=_("Badge category."),
    )
    state = models.IntegerField(
        choices=State.choices,
        default=State.ACTIVE,
        help_text=_("Badge status."),
    )
    icon = models.CharField(
        default="",
        max_length=250,
        help_text=_("The icon to display for the badge."),
    )
    date = models.DateTimeField(
        default=timezone.now,
        help_text=_("First created"),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Set the date to current time if missing.
        self.uid = self.uid or utils.get_uid(limit=8)
        if not self.slug:
            utils.unique_slugify(self, self.name)
        super(Badge, self).save(*args, **kwargs)


class Award(models.Model):
    """
    A badge being awarded to a user.
    Cannot be ManyToManyField because some may be earned multiple times
    """

    uid = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        related_name="awards",
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        default=timezone.now,
        help_text=_("Earned date"),
    )

    def __str__(self):
        return str(self.badge)

    def save(self, *args, **kwargs):
        # Set the date to current time if missing.
        self.uid = self.uid or utils.get_uid(limit=8)
        super().save(*args, **kwargs)


class Reaction(models.Model):
    class Type(models.IntegerChoices):
        EMPTY = 99, _("empty")
        UP = 0, _("up vote")
        DOWN = 1, _("down vote")
        BOOKMARK = 3, _("bookmark")
        ACCEPT = 4, _("accept")
        SPAM = 5, _("spam")

        __empty__ = _("(unknown)")

    ALLOWED_REACTION_MAP = {
        Question: [
            Type.UP,
            Type.DOWN,
            Type.BOOKMARK,
            Type.SPAM,
        ],
        Tutorial: [
            Type.BOOKMARK,
            Type.SPAM,
        ],
        Comment: [
            Type.UP,
            Type.DOWN,
            Type.SPAM,
        ],
        Help: [
            Type.BOOKMARK,
        ],
    }

    uid = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        related_name="reactions",
        on_delete=models.CASCADE,
    )
    page = models.ForeignKey(
        Page,
        related_name="reactions",
        on_delete=models.CASCADE,
    )
    type = models.IntegerField(
        choices=Type.choices,
        default=Type.__empty__,
        null=True,
        blank=True,
        db_index=True,
    )
    date = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )
    objects = ReactionManager()

    def __str__(self):
        return "Reaction: %s, %s, %s" % (self.page.id, self.user, self.get_type_display())

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_uid(8)
        self.date = self.date or timezone.now()
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.uid,)


class Visitor(models.Model):
    """
    Track of post views based on IP address.
    """

    ip = models.GenericIPAddressField(default="", null=True, blank=True)
    page = models.ForeignKey(Page, related_name="visitors", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)


class AbstractProfile(models.Model):
    class Role(models.IntegerChoices):
        READER = 1, _("reader")
        MODERATOR = 2, _("moderator")
        MANAGER = 3, _("manager")
        BLOGGER = 4, _("blogger")

    class State(models.IntegerChoices):
        NEW = 1, _("new")
        TRUSTED = 2, _("trusted")
        SUSPENDED = 3, _("suspended")
        BANNED = 4, _("banned")
        SPAMMER = 5, _("spammer")

    class Messaging(IntegerChoices):
        LOCAL_MESSAGE = 1, _("local messages")
        EMAIL_MESSAGE = 2, _("email")
        NO_MESSAGES = 3, _("no messages")
        DEFAULT_MESSAGES = 4, _("default")

    uid = models.CharField(
        max_length=MAX_UID,
        unique=True,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    role = models.IntegerField(
        default=Role.READER,
        choices=Role.choices,
        verbose_name=_("role"),
        db_index=True,
    )
    avatar = models.ImageField(
        upload_to="avatar",
        null=True,
        blank=True,
        verbose_name=_("avatar"),
    )
    bio = models.TextField(
        default="No profile information",
        null=True,
        max_length=245,
        blank=True,
        help_text=_("description provided by the user."),
    )
    city = models.CharField(
        default="",
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("city"),
    )
    region = models.CharField(
        default="",
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("region"),
    )
    location = models.CharField(
        default="",
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text=_(
            "User provided location.",
        ),
    )
    message = models.IntegerField(
        choices=Messaging.choices,
        default=Messaging.DEFAULT_MESSAGES,
        help_text=_("Messaging profile"),
    )
    my_tags = models.CharField(
        default="",
        max_length=MAX_TEXT,
        blank=True,
        help_text=_("This field is used to select content for the user."),
    )
    watched_tags = models.CharField(
        max_length=MAX_TEXT,
        default="",
        blank=True,
        help_text=_("The tag value is the canonical form of the post's tags"),
    )
    watched = TaggableManager(through=TaggedItem, blank=True)
    new_messages = models.IntegerField(
        default=0,
        db_index=True,
        help_text=_("The number of new messages for the user."),
    )
    score = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
        help_text=_("User reputation score."),
    )
    last_login = models.DateTimeField(
        null=True,
        max_length=255,
        db_index=True,
        help_text=_("The date the user last logged in."),
    )
    subscriber_count = models.IntegerField(default=0, editable=False)
    state = models.IntegerField(
        default=State.NEW,
        choices=State.choices,
        db_index=True,
    )
    last_login = models.DateTimeField(
        null=True,
        default=timezone.now,
        max_length=255,
        db_index=True,
        help_text=_("The date the user last logged in."),
    )

    def __str__(self):
        return "%s profile" % self.user

    @property
    def mailing_list(self):
        """
        User has mailing list mode turned on.
        """
        return self.digest_prefs == self.ALL_MESSAGES

    @property
    def is_moderator(self):
        # Managers can moderate as well.
        return (
            self.role == self.Role.MODERATOR
            or self.role == self.Role.MANAGER
            or self.user.is_staff
            or self.user.is_superuser
        )

    @property
    def trusted(self):
        return (
            self.user.is_staff
            or self.state == self.State.TRUSTED
            or self.role == self.Role.MODERATOR
            or self.role == self.Role.MANAGER
            or self.user.is_superuser
        )

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @cached_property
    def my_tags_list(self):
        return parse_tags(self.my_tags)

    @cached_property
    def full_name(self):
        if self.user.first_name:
            return " ".join([self.user.first_name, self.user.last_name])
        else:
            return self.username

    def get_score(self):
        """ """
        score = self.score * 10
        return score

    def add_watched(self):
        try:
            tags = [Tag.objects.get_or_create(name=name)[0] for name in parse_tags(self.watched_tags)]
            self.watched.clear()
            self.watched.add(*tags)
        except Exception as exc:
            logger.error(f"recomputing watched tags={exc}")

    def save(self, *args, **kwargs):
        self.uid = self.uid or utils.get_uid(8)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Profile(AbstractProfile):
    class Meta:
        swappable = "SLUNIC_PROFILE_MODEL"


class Subscription(models.Model):
    "Connects a post to a user"

    class Type(models.IntegerChoices):
        LOCAL_MESSAGE = 1, _("local messages")
        EMAIL_MESSAGE = 2, _("email message")
        NO_MESSAGES = 3, _("not subscribed")

    TYPE_MAP = {
        Profile.Messaging.NO_MESSAGES: Type.NO_MESSAGES,
        Profile.Messaging.EMAIL_MESSAGE: Type.EMAIL_MESSAGE,
        Profile.Messaging.LOCAL_MESSAGE: Type.LOCAL_MESSAGE,
        Profile.Messaging.DEFAULT_MESSAGES: Type.LOCAL_MESSAGE,
    }

    user = models.ForeignKey(
        User,
        related_name="subscribers",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    subs = models.ForeignKey(
        User,
        related_name="follows",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    type = models.IntegerField(
        choices=Type.choices,
        null=True,
        default=Type.LOCAL_MESSAGE,
    )
    date = models.DateTimeField()

    class Meta:
        unique_together = ("user", "subs")

    def __str__(self):
        return f"{self.user.profile.name} to {self.post.title}"

    def save(self, *args, **kwargs):
        # Set the date to current time if missing.
        self.date = self.date or timezone.now()
        # self.uid = self.uid or util.get_uuid(limit=16)

        if self.type is None:
            self.type = self.TYPE_MAP.get(self.user.profile.message, self.NO_MESSAGES)

        super(Subscription, self).save(*args, **kwargs)

    def profile_type_mapper(self):
        type_map = {
            Profile.NO_MESSAGES: self.NO_MESSAGES,
            Profile.EMAIL_MESSAGE: self.EMAIL_MESSAGE,
            Profile.LOCAL_MESSAGE: self.LOCAL_MESSAGE,
            Profile.DEFAULT_MESSAGES: self.LOCAL_MESSAGE,
        }
        return type_map

    @staticmethod
    def get_sub(post, user):
        sub = Subscription.objects.filter(post=post, user=user).first()
        return None if user.is_anonymous else sub


class Log(models.Model):
    """
    Represents moderation actions
    """

    MODERATE, CREATE, EDIT, LOGIN, LOGOUT, CLASSIFY, DEFAULT = range(7)

    ACTIONS_CHOICES = [
        (MODERATE, "Moderate"),
        (CREATE, "Create"),
        (EDIT, "Edit"),
        (LOGIN, "Login"),
        (LOGOUT, "Logout"),
        (CLASSIFY, "Classify"),
        (DEFAULT, "Default"),
    ]

    # User that performed the action.
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # A potential target user (it may be null)
    target = models.ForeignKey(User, related_name="target", null=True, blank=True, on_delete=models.CASCADE)

    # Page related information goes here (it may be null).
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.CASCADE)

    # The IP address associated with the log.
    ipaddr = models.GenericIPAddressField(null=True, blank=True)

    # Actions that the user took.
    action = models.IntegerField(choices=ACTIONS_CHOICES, default=DEFAULT, db_index=True)

    # The logging information.
    text = models.TextField(null=True, blank=True)

    # Date this log was created.
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.date = self.date or timezone.now()
        super().save(*args, **kwargs)
