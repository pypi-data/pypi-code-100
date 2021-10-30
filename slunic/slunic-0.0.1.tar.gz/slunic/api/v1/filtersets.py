import django_filters as filters
from django_filters.rest_framework import FilterSet

from slunic.models import Comment, Help, Page, Question, Tutorial
from taggit.forms import TagField

NEW = "new"
HOT = "hot"
IMPORTANT = "important"
INTEREST = "interest"
POPULAR = "popular"

TREND_CHOICES = (
    ("new", "News"),
    ("hot", "Hot"),
    ("interest", "Interest"),
    ("important", "Important"),
    ("popular", "Popular"),
)


class TagFilter(filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, **kwargs)


class PageFilterSet(FilterSet):
    class Meta:
        model = Page
        fields = [
            "parent",
            "author",
            "edited_by",
            "level",
            "tree_id",
            "created_at",
        ]


class HelpFilterSet(PageFilterSet):
    class Meta(PageFilterSet.Meta):
        model = Help


class TutorialFilterSet(FilterSet):
    tags = TagFilter(field_name="tags__name")
    popular = filters.ChoiceFilter(choices=TREND_CHOICES, method="get_trend_filter")

    class Meta:
        model = Tutorial
        fields = [
            "parent",
            "author",
            "edited_by",
            "level",
            "tree_id",
            "created_at",
            "tags",
        ]

    def get_trend_filter(self, queryset, name, value):
        qs = queryset
        if value == NEW:
            return qs
        if value == HOT:
            return qs.order_by("-view_count")
        if value == POPULAR:
            return qs.order_by("-vote_count")
        if value == IMPORTANT:
            return qs.order_by("-bookmark_count")
        if value == INTEREST:
            tags = self.request.user.profile.my_tags_list
            return qs.filter(tags__in=tags)


class QuestionFilterSet(PageFilterSet):
    tags = TagFilter(field_name="tags__name")
    popular = filters.ChoiceFilter(choices=TREND_CHOICES, method="get_trend_filter")

    class Meta(PageFilterSet.Meta):
        model = Question
        fields = [
            "parent",
            "author",
            "edited_by",
            "level",
            "tree_id",
            "created_at",
            "tags",
        ]

    def get_trend_filter(self, queryset, name, value):
        qs = queryset
        if value == NEW:
            return qs
        if value == HOT:
            return qs.order_by("-view_count")
        if value == POPULAR:
            return qs.order_by("-vote_count")
        if value == IMPORTANT:
            return qs.order_by("-bookmark_count")
        if value == INTEREST:
            tags = self.request.user.profile.my_tags_list
            return qs.filter(tags__in=tags)


class CommentFilterSet(PageFilterSet):
    class Meta(PageFilterSet.Meta):
        model = Comment
