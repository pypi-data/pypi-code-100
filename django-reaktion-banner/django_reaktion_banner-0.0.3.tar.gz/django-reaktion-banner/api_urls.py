from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .api import API_BannerView, API_BannerTotalClicks

app_name = 'banners-api'
urlpatterns = [
    path('banner/<int:banner_id>/view', API_BannerView.as_view(), name="view" ),
    path('banner/<int:banner_id>/click', API_BannerTotalClicks.as_view(), name="save_click" ),
] 

urlpatterns = format_suffix_patterns(urlpatterns)
