from django.urls import path
from .views import *

app_name = "crypto_auth"

urlpatterns = [

    ## COINBASE

    path('coinbase/confirm_auth', confirm_auth_coinbase, name="confirm_auth"),
]