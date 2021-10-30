import re
from django.core.cache import cache
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TagList, TaggitSerializer

from slunic import models, markdown as md
from slunic.utils import get_gravatar_url, get_profile_model
from slunic.helpers import handle_comment

Profile = get_profile_model()


class DisplayChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value == "" and self.allow_blank:
            return value
        for val, lbl in self._choices.items():
            if val == value:
                return {"value": val, "label": lbl}

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class DisplayIntegerChoiceField(serializers.ChoiceField):

    re_decimal = re.compile(r"\.0*\s*$")

    def to_representation(self, value):
        if value is None and self.allow_blank:
            return int(value)
        for val, lbl in self._choices.items():
            if val == int(value):
                return {"value": int(val), "label": lbl}

    def to_internal_value(self, data):
        # To support inserts with the value
        if data is None and self.allow_blank:
            return None
        try:
            data = int(self.re_decimal.sub("", str(data)))
        except (ValueError, TypeError):
            self.fail("invalid")

        for key, val in self._choices.items():
            if key == data:
                return key
        self.fail("invalid_choice", input=data)


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "avatar")

    def get_avatar(self, obj):
        return get_gravatar_url(obj.email, size=50)


class TagListCharField(TagListSerializerField, serializers.ListField):
    child = serializers.CharField()


class TagListJSONField(TagListCharField):
    child = serializers.JSONField()

    def to_representation(self, value):
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                if self.order_by:
                    tags = value.all().order_by(*self.order_by)
                else:
                    tags = value.all()
                value = [{"id": tag.id, "name": tag.name} for tag in tags]
            value = TagList(value, pretty_print=self.pretty_print)

        return value


class TagSerializer(serializers.ModelSerializer):
    tagged_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Tag
        fields = "__all__"

    def get_tagged_count(self, obj):
        return obj.tagged_count


class CategorySerializer(serializers.ModelSerializer):
    tutorials_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        exclude = ("parent", "rght", "lft")

    def get_tutorials_count(self, obj):
        return obj.tutorials.count()


class CategoryRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ("parent", "rght", "lft")


class CategoryCreateSerializer(serializers.ModelSerializer):
    parent = CategorySerializer()

    class Meta:
        model = models.Category
        fields = ("id", "parent", "name", "slug", "description")


class ParentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Page
        fields = (
            "id",
            "slug",
            "seo_title",
            "seo_description",
            "created_at",
            "author",
        )


class PageStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        exclude = (
            "lft",
            "rght",
            "title",
            "content",
            "seo_title",
            "seo_description",
            "author",
            "edited_by",
            "parent",
        )


class HelpSerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    author = UserSerializer()
    edited_by = UserSerializer()
    category = CategorySerializer()
    html = serializers.SerializerMethodField()

    class Meta:
        model = models.Help
        exclude = ("lft", "rght")

    def get_html(self, obj):
        return md.parse(obj.content)


class HelpEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Help
        fields = (
            "parent",
            "title",
            "content",
            "category",
            "seo_title",
            "seo_description",
        )


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    parent = ParentSerializer()
    author = UserSerializer()
    edited_by = UserSerializer()
    state = DisplayIntegerChoiceField(choices=models.Question.State.choices)
    tags = TagListJSONField()
    answer_count = serializers.SerializerMethodField()
    comment_allowed = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        exclude = ("lft", "rght")

    def get_answer_count(self, obj):
        return obj.get_descendant_count()

    def get_comment_allowed(self, obj):
        return obj.comment_allowed

    def get_html(self, obj):
        return md.parse_simple(obj.content)

    def get_url(self, obj):
        return obj.get_absolute_url()


class QuestionEditSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListCharField()

    class Meta:
        model = models.Question
        fields = (
            "title",
            "content",
            "tags",
        )


class TutorialSimpleSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Tutorial
        fields = ("id", "author", "title", "slug", "summary", "created_at")


class TutorialSerializer(TaggitSerializer, serializers.ModelSerializer):
    parent = ParentSerializer()
    author = UserSerializer()
    edited_by = UserSerializer()
    category = CategoryRelatedSerializer()
    tags = TagListJSONField()
    edited_by = UserSerializer()
    comment_allowed = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Tutorial
        exclude = ("lft", "rght", "comment_enabled")
        read_only_fields = ("author", "edited_by")

    def get_reaction_states(self, obj):
        request = self.context["request"]
        cache_key = f"PageUserReactions:{obj.id}:{request.user.id}"
        reactions = cache.get(cache_key)
        if reactions:
            return reactions
        else:
            reactions = obj.get_reaction_states(request.user)
            cache.set(cache_key, reactions, 60)
        return reactions

    def get_html(self, obj):
        return md.parse(obj.content)

    def get_comment_allowed(self, obj):
        return obj.comment_allowed

    def get_url(self, obj):
        return obj.get_absolute_url()


class TutorialEditSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListCharField()

    class Meta:
        model = models.Tutorial
        fields = (
            "title",
            "summary",
            "content",
            "tags",
            "seo_title",
            "seo_description",
        )
        extra_kwargs = {
            "seo_title": {"required": False},
        }

    def validate(self, attrs):
        instance = models.Tutorial(**attrs)
        instance.clean()
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    author = UserSerializer()
    edited_by = UserSerializer()
    type = DisplayIntegerChoiceField(choices=models.Comment.Type.choices)
    comment_count = serializers.SerializerMethodField()
    comment_allowed = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        exclude = ("lft", "rght", "comment_enabled")

    def get_comment_count(self, obj):
        return obj.get_descendant_count()

    def get_comment_allowed(self, obj):
        return obj.comment_allowed

    def get_html(self, obj):
        return md.parse_simple(obj.content)


class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("parent", "content")

    def validate(self, attrs):
        instance = models.Comment(**attrs)
        instance.clean()
        return attrs

    def get_user(self):
        user = None
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            user = request.user
            return user
        raise

    def create(self, validated_data):
        user = self.get_user()
        parent = validated_data["parent"]
        content = validated_data["content"]
        instance = handle_comment(user, parent, content, instance=None)
        return instance

    def update(self, instance, validated_data):
        user = self.get_user()
        parent = validated_data["parent"]
        content = validated_data["content"]
        instance = handle_comment(user, parent, content, instance=instance)
        return instance


class BadgeSerializer(serializers.ModelSerializer):
    level = DisplayChoiceField(choices=models.Badge.Level.choices)
    category = DisplayChoiceField(choices=models.Badge.Category.choices)
    state = DisplayChoiceField(choices=models.Badge.State.choices)

    class Meta:
        model = models.Badge
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()
    user = UserSerializer()

    class Meta:
        model = models.Award
        fields = "__all__"


class ReactionSerializer(serializers.ModelSerializer):
    type = DisplayChoiceField(models.Reaction.Type.choices)

    class Meta:
        model = models.Reaction
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Visitor
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    my_tags_list = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Profile
        exclude = ("avatar", "my_tags")

    def get_my_tags_list(self, obj):
        return obj.my_tags_list

    def get_full_name(self, obj):
        return obj.full_name


class NotificationSerializer(serializers.Serializer):
    recipient = UserSerializer(models.User, read_only=True)
    unread = serializers.BooleanField(read_only=True)
