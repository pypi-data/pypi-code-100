from slunic import hooks
from slunic.configs import app_configs
from slunic.api.v1 import views

API_VIEWS_HOOK_V1 = app_configs.API_VIEWS_HOOK_V1
API_VIEWSETS_HOOK_V1 = app_configs.API_VIEWSETS_HOOK_V1


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_server_viewset():
    return ("stats", views.StatViewSet, "stats")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_author_viewset():
    return ("profile", views.ProfileViewSet, "profile")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_tag_viewset():
    return ("tag", views.TagViewSet, "tag")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_category_viewset():
    return ("category", views.CategoryViewSet, "category")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_help_viewset():
    return ("help", views.HelpViewSet, "help")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_tutorial_viewset():
    return ("tutorial", views.TutorialViewSet, "tutorial")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_question_viewset():
    return ("question", views.QuestionViewSet, "question")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_comment_viewset():
    return ("comment", views.CommentViewSet, "comment")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_badge_viewset():
    return ("badge", views.BadgeViewSet, "badge")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_award_viewset():
    return ("award", views.AwardViewSet, "award")


@hooks.register(API_VIEWSETS_HOOK_V1)
def register_reaction_viewset():
    return ("reaction", views.ReactionViewSet, "reaction")
