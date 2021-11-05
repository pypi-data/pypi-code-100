from django.urls import path, include

from . import views


app_name = 'groups'


ajax_urls = [
    path('table/<str:type>/', views.ReportGroupListView.as_view(), name='list'),
    path('create/', views.ReportGroupCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ReportGroupUpdateView.as_view(), name='update'),
]


urlpatterns = [
    path('', views.ReportGroupListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('ajax/', include(ajax_urls)),
]
