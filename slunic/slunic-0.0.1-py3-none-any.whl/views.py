from django.apps import apps
from django.core.exceptions import BadRequest

# from django.core.cache import cache
from django.http.response import Http404
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.utils import translation
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import get_object_or_404

from slunic.api import DEFAULT_VIEWSETS
from slunic.configs import app_configs
from slunic.forms import CommentForm, TutorialForm, QuestionForm

APP_NAME = app_configs.APP_NAME
THEME_NAME = app_configs.THEME_NAME

EDIT_FORM_MAP = {
    "tutorial": TutorialForm,
    "question": QuestionForm,
}

_ = translation.gettext_lazy


class Maintenance(TemplateView):
    template_name = "maintenance.html"


class BaseView(TemplateView):

    page_title = "Page Title"
    page_subtitle = "Page Subtitle"

    def get_context_data(self, **kwargs):
        kwargs["page_title"] = self.get_page_title()
        kwargs["page_subtitle"] = self.get_page_subtitle()
        return super().get_context_data(**kwargs)

    def get_page_title(self):
        return self.page_title

    def get_page_subtitle(self):
        return self.page_subtitle


class Index(BaseView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        return [
            "%s/%s/index.html" % (APP_NAME, THEME_NAME),
            "%s/index.html" % THEME_NAME,
            "%s/index.html" % APP_NAME,
            self.template_name,
        ]


class PageList(BaseView):
    template_name = "list.html"

    def dispatch(self, request, model_name, *args, **kwargs):
        self.model_name = model_name
        self.page = request.GET.get("page", 1)
        if self.model_name not in app_configs.MODELS_FOR_LIST:
            raise Http404(_("Invalid content type '%s'.") % self.model_name)
        return super().dispatch(request, model_name, *args, **kwargs)

    def get_page_title(self):
        return "%ss" % self.model_name.title()

    def get_page_subtitle(self):
        if self.model_name == "tutorial":
            return _("Supporting each other to make an impact. Start to share your knowledge.")
        elif self.model_name == "question":
            return _("Find the best answer to your technical question, help others answer theirs.")
        elif self.model_name == "tag":
            return _(
                "A tag is a keyword or label that categorizes your question with other, similar questions."
                "Using the right tags makes it easier for others to find tutorial and answer your question."
            )
        elif self.model_name == "badge":
            return _(
                "Besides gaining reputation with your questions and answers, you receive "
                "badges for being especially helpful. Badges appear on your profile page, "
                "flair, and your posts."
            )
        else:
            return super().get_page_subtitle()

    def get_data(self):
        viewset = DEFAULT_VIEWSETS[self.model_name]
        view = viewset.as_view({"get": "list"})(self.request)
        return view.data

    def get_context_data(self, **kwargs):
        kwargs["model_name"] = self.model_name
        kwargs.update(self.get_data())
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        return [
            "%s/%s/%s/list.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/%s_list.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/list.html" % (APP_NAME, THEME_NAME),
            "%s/%s/list.html" % (APP_NAME, self.model_name),
            "%s/%s_list.html" % (APP_NAME, self.model_name),
            "%s/list.html" % APP_NAME,
            self.template_name,
        ]


class PageDetail(BaseView, FormView):

    form_class = CommentForm

    def dispatch(self, request, model_name, id, slug, *args, **kwargs):
        self.model_name = model_name
        self.id = id
        self.slug = slug
        try:
            self.model = apps.get_model("slunic", self.model_name)
        except LookupError:
            raise Http404("%s not found" % self.model_name)
        self.object = get_object_or_404(self.model, pk=self.id)
        self.comment_enabled = self.model_name in app_configs.MODELS_FOR_COMMENT
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["page"] = self.object
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        kwargs["object"] = self.object
        kwargs["model_name"] = self.model_name
        kwargs["page_title"] = self.get_page_title()
        kwargs["page_subtitle"] = self.get_page_subtitle()
        if self.comment_enabled:
            kwargs["form"] = self.get_form()
        return kwargs

    def get_template_names(self):
        return [
            "%s/%s/%s/detail.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/%s.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/%s_detail.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s.html" % (APP_NAME, self.model_name),
            "%s/%s_detail.html" % (APP_NAME, self.model_name),
            "%s/detail.html" % APP_NAME,
            self.template_name,
        ]

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_success_message(self, obj):
        return messages.success(self.request, _("Your %s created.") % obj._meta.model_name)

    def form_valid(self, form=None):
        comment = form.save()
        self.get_success_message(comment)
        return super().form_valid(form)

    def form_invalid(self, form=None):
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data(kwargs=kwargs))

    def post(self, request, *args, **kwargs):
        if self.comment_enabled:
            return super().post(request, *args, **kwargs)
        else:
            raise BadRequest()


@method_decorator([login_required], name="dispatch")
class PageCreate(BaseView, FormView):
    def dispatch(self, request, model_name, *args, **kwargs):
        self.model_name = model_name
        if self.model_name not in ["tutorial", "question"]:
            raise Http404(_("Invalid submission for '%s'.") % self.model_name)
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return EDIT_FORM_MAP[self.model_name]

    def get_context_data(self, **kwargs):
        kwargs["model_name"] = self.model_name
        kwargs["action"] = _("create")
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        url = reverse(
            "slunic_page_detail",
            kwargs={
                "id": self.request.user.id,
                "slug": self.request.user.username,
                "model_name": "profile",
            },
        )
        return url

    def get_success_message(self):
        return messages.success(self.request, _("Your %s created.") % self.model_name)

    def get_template_names(self):
        return [
            "%s/%s/%s/form.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/forms/%s.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/%s/%s_form.html" % (APP_NAME, THEME_NAME, self.model_name),
            "%s/forms/%s.html" % (APP_NAME, self.model_name),
            "%s/%s_form.html" % (APP_NAME, self.model_name),
            "%s/form.html" % APP_NAME,
        ]

    def form_valid(self, form):
        form.save(self.request)
        self.get_success_message()
        return super().form_valid(form)
