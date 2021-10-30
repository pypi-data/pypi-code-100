from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from slunic.utils import get_profile_model

from .models import (
    Reaction,
    Award,
    Badge,
    Category,
    Diff,
    Page,
    Subscription,
    Tag,
    Comment,
    Help,
    Tutorial,
    Question,
    Visitor,
)

Profile = get_profile_model()


class BasePageAdmin(admin.ModelAdmin):
    raw_id_fields = ["parent"]
    fieldset_add = [
        None,
        {"fields": ("parent", "data")},
    ]
    fieldset_base = [
        _("Options"),
        {
            "classes": ("collapse",),
            "fields": (
                "seo_title",
                "seo_description",
                "login_required",
                "comment_enabled",
                "template_name",
            ),
        },
    ]

    def save_model(self, request, obj, form, change):
        """Add user to object"""
        if obj.author is None:
            obj.author = request.user
        if change:
            obj.last_edited_at = timezone.now()
            obj.edited_by = request.user
        return super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj):
        if self.fieldset_add:
            fieldsets = [self.fieldset_add, self.fieldset_base]
        else:
            fieldsets = [self.fieldset_base]
        return fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


@admin.register(Page)
class PageAdmin(BasePageAdmin):
    list_display = ["slug", "parent_id", "tree_id", "level", "lft", "rght", "real_model", "descendants"]
    search_fields = ["tree_id"]

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj=obj)

    def descendants(self, obj):
        return obj.get_descendant_count()


@admin.register(Tutorial)
class TutorialAdmin(BasePageAdmin):
    search_fields = ("title__icontain", "content__icontain")
    list_display = ["title", "parent", "created_at", "last_edited_at", "is_live", "real_model"]
    list_filter = ["category", "created_at", "is_live"]
    fieldset_add = [
        None,
        {"fields": ("parent", "category", "tags", "title", "summary", "content", "data")},
    ]


@admin.register(Help)
class HelpAdmin(BasePageAdmin):
    search_fields = ("title__icontain", "content__icontain")
    list_display = ["title", "parent", "created_at", "last_edited_at", "is_live"]
    list_filter = ["category", "created_at", "is_live"]
    fieldset_add = [
        None,
        {"fields": ("parent", "category", "title", "content", "data")},
    ]


@admin.register(Question)
class QuestionAdmin(BasePageAdmin):
    list_display = ["title", "level", "tree_id"]
    list_display = ["title", "parent", "created_at", "last_edited_at", "is_live", "vote_count"]
    list_filter = ["created_at", "is_live"]
    fieldset_add = [
        None,
        {"fields": ("parent", "title", "content", "data", "tags")},
    ]


@admin.register(Comment)
class CommentAdmin(BasePageAdmin):
    list_display = ["parent", "level", "tree_id"]
    fieldset_add = [
        None,
        {"fields": ("parent", "content", "data")},
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "level", "category", "state"]
    list_filter = ["level", "category", "state"]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["user", "page", "badge", "date"]


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ["ip", "page", "date", "city", "region", "country"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "description"]


@admin.register(Subscription)
class SubcriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "subs", "date"]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["user", "page_id", "type", "date"]


@admin.register(Diff)
class DiffAdmin(admin.ModelAdmin):
    list_display = ["page", "author", "created"]
