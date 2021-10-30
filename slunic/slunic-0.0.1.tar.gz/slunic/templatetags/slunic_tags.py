from dateutil.parser import parse as parse_date
from django.conf import settings
from django.http import HttpRequest
from django.template import Library, loader
from django.template.loader import select_template, get_template
from slunic import __version__, models, utils, markdown as md
from slunic.configs import app_configs


register = Library()


class CustomRequest(HttpRequest):
    def __init__(self, user, method, **query):
        self.user = user
        self.GET = query
        self.method = method


def resolve_template(template):
    """Accept a template object, path-to-template, or list of paths."""
    if isinstance(template, (list, tuple)):
        return select_template(template)
    elif isinstance(template, str):
        return get_template(template)
    else:
        return template


@register.simple_tag(takes_context=True)
def slunic_version(context):
    if settings.DEBUG:
        return f"v.{__version__}"
    else:
        return ""


@register.simple_tag(takes_context=True)
def gravatar_url(context, user, size=50):
    return utils.get_gravatar_url(user.email, size=size)


@register.simple_tag
def slunic_login_url():
    return utils.get_login_url()


@register.simple_tag
def slunic_logout_url():
    return utils.get_logout_url()


@register.simple_tag
def slunic_signup_url():
    return utils.get_signup_url()


@register.filter(name="markdown")
def markdown(text):
    return md.parse(text)


@register.filter(name="proper_paginate_api")
def proper_paginate(paginator, current_page, neighbors=3):
    if paginator["num_pages"] > 2 * neighbors:
        start_index = max(1, current_page - neighbors)
        end_index = min(paginator["num_pages"], current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator["num_pages"]:
            start_index -= end_index - paginator["num_pages"]
            end_index = paginator["num_pages"]
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[: (2 * neighbors + 1)]
    return paginator["page_range"]


@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.inclusion_tag(takes_context=True, filename="slunic/includes/comments.html")
def render_comments(context, obj):
    request = context.get("request")
    if obj._meta.model_name in app_configs.MODELS_FOR_COMMENT:
        left = obj.lft + 1
        right = obj.rght - 1
        comments = models.Comment.objects.select_related("parent", "author").filter(
            tree_id=obj.tree_id, lft__gte=left, rght__lte=right, is_spam=False
        )
    else:
        comments = list()
    return {"request": request, "comments": comments}


@register.simple_tag(takes_context=True)
def render_content_type(context, model_name, obj, detail=False):
    request = context.get("request")
    template = [
        "slunic/contents/%s.html" % model_name,
        "slunic/contents/base.html"
    ]
    ctx = {"request": request, "object": obj, "detail": detail}
    content = loader.render_to_string(template, ctx)
    return content


@register.inclusion_tag(takes_context=False, filename="slunic/widgets/popular_tags.html")
def widget_popular_tags(limit=10):
    ctx = {"limit": limit}
    return ctx


@register.inclusion_tag(takes_context=False, filename="slunic/widgets/popular_posts.html")
def widget_popular_posts(model_name, limit=10):
    ctx = {"model_name": model_name, "limit": limit}
    return ctx


@register.inclusion_tag(takes_context=False, filename="slunic/widgets/related_posts.html")
def widget_related_posts(obj, limit=10):
    ctx = {"object": obj, "model_name": obj.real_model, "limit": limit}
    return ctx


@register.inclusion_tag(takes_context=True, filename="slunic/widgets/featured_join.html")
def widget_featured_join(context):
    request = context.get("request")
    return {"request": request}


@register.inclusion_tag(takes_context=True, filename="slunic/widgets/submit_question.html")
def widget_submit_question(context):
    request = context.get("request")
    return {"request": request}


@register.inclusion_tag(takes_context=True, filename="slunic/widgets/submit_tutorial.html")
def widget_submit_tutorial(context):
    request = context.get("request")
    return {"request": request}


@register.filter(name="parse_date")
def date_parse(str):
    return parse_date(str)
