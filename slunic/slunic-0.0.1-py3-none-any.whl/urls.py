from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:model_name>/create/",
        views.PageCreate.as_view(),
        name="slunic_page_create",
    ),
    path(
        "<str:model_name>/<int:id>/<str:slug>/",
        views.PageDetail.as_view(),
        name="slunic_page_detail",
    ),
    path(
        "<str:model_name>/",
        views.PageList.as_view(),
        name="slunic_page_list",
    ),
    path(
        "",
        view=views.Index.as_view(),
        name="slunic_index",
    ),
]
