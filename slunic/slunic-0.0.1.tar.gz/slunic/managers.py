from django.db import models
from django.db.models.aggregates import Count
from mptt.managers import TreeManager


class TagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("slunic_taggeditem_items")
        count = Count("slunic_taggeditem_items", distinct=True)
        return (
            qs.prefetch_related("slunic_taggeditem_items")
            .annotate(tagged_count=count)
            .order_by("name")
        )

    def popular(self):
        return self.get_queryset().order_by("-tagged_count")


class ProfileManager(models.Manager):
    def valid_users(self):
        """
        Return valid user queryset, filtering new and trusted users.
        """
        query = (
            super()
            .get_queryset()
            .filter(
                models.Q(state=self.model.State.TRUSTED) | models.Q(state=self.model.State.NEW),
            )
        )
        return query


class CategoryManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("parent")


class PageManager(TreeManager):
    def live(self):
        return self.filter(is_spam=False, deleted=False, is_live=True)

    def get_by_natural_key(self, uid):
        return self.get(uid=uid)


class ReactionManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.select_related("user", "page")


class TutorialManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs
