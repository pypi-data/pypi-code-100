from django.urls import path

from . import views

app_name = 'banner'
urlpatterns = [
    path('<int:pk>', views.redirect_to_banner_target, name="redirect"),
]
