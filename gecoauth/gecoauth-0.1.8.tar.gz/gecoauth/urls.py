from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import GecoRegisterView

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/registration/', GecoRegisterView.as_view()),
]