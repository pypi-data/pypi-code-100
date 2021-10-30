from django.utils import timezone
from haystack import indexes

from .models import Comment, Tutorial, Question, Help  # NOQA


class TutorialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="slunic/search/search_post.txt",
    )
    title = indexes.CharField(model_attr="title")
    author = indexes.CharField(model_attr="author")
    created_at = indexes.DateTimeField(model_attr="created_at")

    def get_model(self):
        return Tutorial

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="slunic/search/search_post.txt",
    )
    title = indexes.CharField(model_attr="title")
    author = indexes.CharField(model_attr="author")
    created_at = indexes.DateTimeField(model_attr="created_at")

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())


class HelpIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="slunic/search/search_post.txt",
    )
    title = indexes.CharField(model_attr="title")
    author = indexes.CharField(model_attr="author")
    created_at = indexes.DateTimeField(model_attr="created_at")

    def get_model(self):
        return Help

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="slunic/search/search_response.txt",
    )
    author = indexes.CharField(model_attr="author")
    created_at = indexes.DateTimeField(model_attr="created_at")

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())
