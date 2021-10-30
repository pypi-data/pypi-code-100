from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from slunic import __version__, models, utils
from slunic.helpers import handle_vote
from slunic.api.paginations import CachedPageNumberPagination
from slunic.configs import app_configs
from . import serializers, permissions, filtersets


Profile = utils.get_profile_model()


class CachedReadOnlyModelViewSet(ReadOnlyModelViewSet):
    pagination_class = CachedPageNumberPagination

    @property
    def model(self):
        return self.get_model()

    @property
    def opts(self):
        return self.model._meta

    @property
    def model_name(self):
        return f"{self.opts.app_label}.{self.opts.model_name}"

    def get_model(self):
        qs = super().get_queryset()
        return qs.model

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        timeout = app_configs.CACHE_OBJECT_DETAIL_TIMEOUT
        cache_key = utils.make_fragment_key(self.model_name, mode="api", page_id=id)
        data = cache.get(cache_key)
        if not data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(cache_key, serializer.data, timeout)
        return Response(data)


class CachedModelViewSet(CachedReadOnlyModelViewSet, ModelViewSet):
    pass


class PageViewSetMixin:
    owner_field = "author"
    create_serializer_class = None
    edit_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return self.edit_serializer_class or self.serializer_class
        elif self.action == "create":
            return self.create_serializer_class or self.edit_serializer_class or self.serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        return instance

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user)


class CommentEnabledMixin:
    def get_serializer_class(self):
        if self.action == "comments":
            return serializers.CommentSerializer
        return super().get_serializer_class()

    @action(methods=["GET"], detail=True)
    def comments(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=pk)
        left = instance.lft + 1
        right = instance.rght - 1
        selects = ("author", "parent__author", "edited_by", "page_ptr")
        queryset = models.Comment.objects.select_related(*selects).filter(
            tree_id=instance.tree_id, lft__gte=left, rght__lte=right, is_spam=False
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HelpViewSet(PageViewSetMixin, CachedModelViewSet):
    queryset = models.Help.objects.all()
    serializer_class = serializers.HelpSerializer
    edit_serializer_class = serializers.HelpEditSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = filtersets.HelpFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "related":
            only = ["id", "category", "category__parent", "author", "title", "slug", "summary", "created_at"]
            return qs.select_related("author").only(*only)
        selects = ("author", "category", "category__parent", "parent", "edited_by", "page_ptr")
        return qs.select_related(*selects).order_by("-created_at")


class TutorialViewSet(CommentEnabledMixin, PageViewSetMixin, CachedModelViewSet):
    queryset = models.Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    edit_serializer_class = serializers.TutorialEditSerializer

    filterset_class = filtersets.TutorialFilterSet

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [permissions.IsTutorOrAdmin()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "related":
            only = ["id", "category", "category__parent", "author", "title", "slug", "summary", "created_at"]
            return qs.select_related("author").only(*only)
        selects = ("author", "category", "category__parent", "parent", "edited_by", "page_ptr")
        return qs.select_related(*selects).prefetch_related("tags").order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "related":
            return serializers.TutorialSimpleSerializer
        return super().get_serializer_class()

    def get_response_serializer(self, instance):
        serializer = self.serializer_class(
            instance=instance,
            context={"request": self.request},
        )
        return serializer

    @action(methods=["GET"], detail=True)
    def related(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(models.Tutorial, pk=pk)
        tags = instance.tags.values("pk")
        qs = self.get_queryset()
        related_tuts = qs.filter(tags__in=tags).exclude(pk=instance.id).distinct()[:20]
        srz_class = self.get_serializer_class()
        srz = srz_class(instance=related_tuts, many=True)
        return Response(data=srz.data)


class QuestionViewSet(CommentEnabledMixin, PageViewSetMixin, CachedModelViewSet):
    queryset = models.Question.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.QuestionSerializer
    edit_serializer_class = serializers.QuestionEditSerializer
    filterset_class = filtersets.QuestionFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        selects = ("author", "parent", "edited_by", "page_ptr")
        return qs.select_related(*selects).prefetch_related("tags").order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "comments":
            return serializers.CommentSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_response_serializer(instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(methods=["GET"], detail=True)
    def related(self, request, pk, *args, **kwargs):
        qs = self.get_queryset()
        instance = get_object_or_404(models.Question, pk=pk)
        tags = instance.tags.values("pk")
        queryset = qs.filter(tags__in=tags).exclude(pk=instance.id).distinct()[:20]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(PageViewSetMixin, ModelViewSet):
    select_related = ("author", "parent__author", "edited_by", "page_ptr")
    queryset = models.Comment.objects.select_related(*select_related)
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    edit_serializer_class = serializers.CommentEditSerializer
    filterset_class = filtersets.CommentFilterSet

    def get_serializer_class(self):
        if self.action == "submit":
            return serializers.CommentEditSerializer
        return super().get_serializer_class()


class StatViewSet(GenericViewSet):
    @action(methods=["GET"], detail=False)
    def version(self, request):
        data = {"version": __version__}
        return Response(data=data, status=status.HTTP_200_OK)


class ProfileViewSet(CachedReadOnlyModelViewSet):
    queryset = models.Profile.objects.select_related("user")
    serializer_class = serializers.ProfileSerializer
    pagination_class = CachedPageNumberPagination


class TagViewSet(CachedReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

    @action(methods=["GET"], detail=False)
    def popular(self, request, *args, **kwargs):
        queryset = models.Tag.objects.popular().order_by('-tagged_count')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(CachedReadOnlyModelViewSet):
    queryset = models.Category.objects.prefetch_related("tutorials").select_related("parent")
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class BadgeViewSet(CachedReadOnlyModelViewSet):
    queryset = models.Badge.objects.all()
    serializer_class = serializers.BadgeSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    pagination_class = CachedPageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("level", "category")


class AwardViewSet(CachedReadOnlyModelViewSet):
    owner_field = "user"
    queryset = models.Award.objects.all()
    serializer_class = serializers.AwardSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class ReactionViewSet(GenericViewSet):
    queryset = models.Reaction.objects.all()
    serializer_class = serializers.ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    @action(methods=["POST"], detail=False)
    def submit(self, request):
        Reaction = models.Reaction
        Page = models.Page

        user = request.user
        reaction_type_label = request.data.get("reaction_type")
        page_uid = request.data.get("uid")
        page = get_object_or_404(Page, uid=page_uid)

        type_map = dict(
            upvote=Reaction.Type.UP,
            downvote=Reaction.Type.DOWN,
            bookmark=Reaction.Type.BOOKMARK,
            accept=Reaction.Type.ACCEPT,
            spam=Reaction.Type.SPAM,
        )
        reaction_type = type_map.get(reaction_type_label)

        if page.author == user and reaction_type in [Reaction.Type.UP, Reaction.Type.DOWN]:
            raise PermissionDenied(_("You can't vote on your own post."))

        # Can not accept if user wrote the answer and not top level post.
        not_allowed = page.author == user and not page.get_root().author == user
        if reaction_type == Reaction.Type.ACCEPT and not_allowed:
            raise PermissionDenied(_("You can't accept on your own post."))

        not_moderator = user.is_authenticated and not user.profile.is_moderator
        if page.get_root().author != user and not_moderator and reaction_type == Reaction.Type.ACCEPT:
            return PermissionDenied(
                _("Only moderators or the person asking the question may accept answers.")
            )

        msg, reaction, change = handle_vote(page=page, user=user, reaction_type=reaction_type)

        serializer = serializers.PageStateSerializer(instance=page)
        return Response(data={"detail": msg, "instance": serializer.data}, status=status.HTTP_200_OK)
