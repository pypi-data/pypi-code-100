from django.urls import path, include

from . import views


app_name = 'formats'


ajax_urls = [
    path('table/<str:type>/', views.FormatListView.as_view(), name='list'),
    path('create/', views.FormatCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.FormatUpdateView.as_view(), name='update'),
]


urlpatterns = [
    path('', views.FormatListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('ajax/', include(ajax_urls)),
]
