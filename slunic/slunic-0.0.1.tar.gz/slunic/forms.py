import time
from django import forms
from django.conf import settings
from django.forms.utils import ErrorDict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from taggit.forms import TagField

from slunic.helpers import handle_diff, handle_comment  # NOQA
from slunic.configs import app_configs
from slunic.models import (
    MAX_TAGS_TEXT,
    MIN_CHARS,
    MAX_TITLE,
    MAX_TAGS,
    MIN_CONTENT,
    Comment,
    Question,
    Tutorial,
)


class EasyMDEditor(forms.Textarea):
    """
    EasyMDE implementations

    https://github.com/Ionaru/easy-markdown-editor

    """

    template_name = "easymde/easymde.html"

    class Media:
        css = {
            "all": (
                static("easymde/easymde.min.css"),
                static("easymde/main.css"),
            )
        }
        js = (
            static("easymde/easymde.min.js"),
            static("easymde/main.js"),
        )

    def __init__(self, attrs=None, configs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {"cols": "40", "rows": "3"}
        self.configs = configs
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        script = ""
        output += mark_safe(script)
        return output

    def get_configs(self, custom_configs):
        configs = app_configs.EASY_MDE
        if self.configs:
            configs.update(custom_configs)
        return configs

    def get_context(self, name, value, attrs):
        return {
            "widget": {
                "name": name,
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "value": self.format_value(value),
                "attrs": self.build_attrs(self.attrs, attrs),
                "configs": self.get_configs(self.configs),
                "template_name": self.template_name,
            },
        }


class AdminEasyMDEditor(EasyMDEditor):
    class Media:
        css = {
            "all": (
                static("easymde/easymde.min.css"),
                static("easymde/main.css"),
            )
        }
        js = (
            static("easymde/easymde.min.css"),
            static("easymde/main.css"),
        )


def valid_title(text):
    "Validates form input for titles."
    text = text.strip()
    if not text:
        raise ValidationError(_("Please enter a title"))

    text = text.replace(" ", "")
    if len(text) < MIN_CHARS:
        raise ValidationError(_("Too short, please add more than {MIN_CHARS} characters."))
    if len(text) > MAX_TITLE:
        raise ValidationError(_("Too Long, please add less than {MAX_TITLE} characters."))
    try:
        text.encode("utf-8")
    except Exception as exc:
        raise ValidationError(_("Title contains invalid characters: {exc}")) from exc


def valid_tag(text):
    "Validates form input for tags"

    words = text.split(",")
    if len(words) > MAX_TAGS:
        raise ValidationError(_("You have too many tags (5 allowed)"))


class FormSecurityMixin(forms.Form):
    """
    Form security methods, taken django-contrib-comment :)
    """

    # If you enter anything in this field your comment will be treated as spam
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    uid = forms.CharField(widget=forms.HiddenInput)
    timestamp = forms.IntegerField(widget=forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)

    def __init__(self, page, user, data=None, initial=None, **kwargs):
        self.user = user
        self.page = page
        self.is_spam = False
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super().__init__(data=data, initial=initial, **kwargs)

    def security_errors(self):
        """Return just those errors associated with security"""
        errors = ErrorDict()
        for f in ["honeypot", "timestamp", "security_hash"]:
            if f in self.errors:
                errors[f] = self.errors[f]
        return errors

    def clean_security_hash(self):
        """Check the security hash."""

        security_hash_dict = {
            "uid": self.data.get("uid", ""),
            "timestamp": self.data.get("timestamp", ""),
        }

        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if not constant_time_compare(expected_hash, actual_hash):
            raise forms.ValidationError("Security hash check failed.")
        return actual_hash

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (default is > 2 hours) in the past."""
        ts = self.cleaned_data["timestamp"]
        if time.time() - ts > app_configs.COMMENTS_TIMEOUT:
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict = {
            "uid": str(self.page.uid),
            "timestamp": str(timestamp),
            "security_hash": self.initial_security_hash(timestamp),
        }
        return security_dict

    def initial_security_hash(self, timestamp):
        """
        Generate the initial security hash from self.content_object
        and a (unix) timestamp.
        """
        initial = {"uid": str(self.page.uid), "timestamp": str(timestamp)}
        return self.generate_security_hash(**initial)

    def generate_security_hash(self, uid, timestamp):
        """
        Generate a HMAC security hash from the provided info.
        """
        info = (uid, timestamp)
        key_salt = settings.SECRET_KEY
        value = "-".join(info)
        return salted_hmac(key_salt, value).hexdigest()


class QuestionForm(forms.Form):

    title = forms.CharField(
        label=_("Post Title"),
        max_length=MAX_TITLE,
        min_length=MIN_CHARS,
        validators=[valid_title],
        help_text=_("Enter a descriptive title to promote better answers."),
    )
    content = forms.CharField(widget=EasyMDEditor())
    tags = TagField(
        label=_("Post Tags"),
        max_length=MAX_TAGS_TEXT,
        required=True,
        validators=[valid_tag],
        widget=forms.TextInput(attrs={"id": "tag_val"}),
        help_text=_("Create a new tag by typing a word then adding a comma."),
    )

    def clean_content(self):
        content = self.cleaned_data["content"]
        length = len(content.replace(" ", ""))

        if length < MIN_CHARS:
            raise forms.ValidationError(_("Too short, place add more than %i characters." % MIN_CONTENT))
        return content

    def save(self, request):
        author = request.user
        tags = self.cleaned_data.pop("tags")
        instance = Question(author=author, **self.cleaned_data)
        instance.save()
        for tag in tags:
            instance.tags.add(tag)
        return instance


class TutorialForm(forms.Form):
    title = forms.CharField(
        label=_("Post Title"),
        max_length=MAX_TITLE,
        min_length=MIN_CHARS,
        validators=[valid_title],
        help_text=_("Enter a descriptive title to help people find your tutorial."),
    )
    summary = forms.CharField(widget=forms.Textarea())
    content = forms.CharField(widget=EasyMDEditor())
    tags = TagField(
        label=_("Post Tags"),
        max_length=MAX_TAGS_TEXT,
        required=True,
        validators=[valid_tag],
        widget=forms.TextInput(attrs={"id": "tag_val"}),
        help_text=_("Create a new tag by typing a word then adding a comma."),
    )

    def clean_content(self):
        content = self.cleaned_data["content"]
        length = len(content.replace(" ", ""))

        if length < MIN_CHARS:
            raise forms.ValidationError(_("Too short, place add more than %i characters." % MIN_CONTENT))
        return content

    def save(self, request):
        author = request.user
        tags = self.cleaned_data.pop("tags")
        instance = Tutorial(author=author, **self.cleaned_data)
        instance.save()
        for tag in tags:
            instance.tags.add(tag)
        return instance


class CommentForm(FormSecurityMixin):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100 mb-3",
                "rows": 2,
            }
        ),
        min_length=app_configs.COMMENT_MIN_LENGTH,
        max_length=app_configs.COMMENT_MAX_LENGTH,
        strip=False,
    )

    def clean_content(self):
        content = self.cleaned_data["content"]
        return content

    def clean(self):
        cleaned_data = super().clean()
        if self.user.is_anonymous:
            raise forms.ValidationError("You need to be logged in.")
        if cleaned_data["honeypot"] not in ["", None]:
            self.is_spam = True
        comment = Comment(author=self.user, parent=self.page, content=cleaned_data["content"])
        comment.clean()
        return cleaned_data

    def save(self):
        content = self.cleaned_data["content"]
        comment = handle_comment(self.user, self.page, content, is_spam=self.is_spam)
        return comment


class DiffForm(FormSecurityMixin):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control w-100 mb-3",
                "rows": 2,
            }
        ),
        min_length=app_configs.COMMENT_MIN_LENGTH,
        max_length=app_configs.COMMENT_MAX_LENGTH,
        strip=False,
    )

    def clean_content(self):
        content = self.cleaned_data["content"]
        return content

    def save(self):
        # Set the fields for this post.
        # Note: self.page is object to be edited
        content = self.cleaned_data.get("content", self.page.content)
        instance = handle_diff(page=self.parent, content=content, user=self.user)
        return instance
