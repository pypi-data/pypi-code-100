from django.urls import path, include

from . import views


app_name = 'tables'


ajax_urls = [
    path('create/', views.DBTableCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.DBTableUpdateView.as_view(), name='update'),
    path('<str:type>/', views.DBTableListView.as_view(), name='list'),
    path('<int:pk>/fields/<str:type>/', views.TableFieldsListView.as_view(), name='fields-list'),
    path('fields/<int:pk>/', views.TableFieldUpdateView.as_view(), name='field-update'),
]


urlpatterns = [
    path('', views.DBTableListView.as_view(), name='list', kwargs={'type': 'base'}),
    path('<int:pk>/', views.DBTableDetailView.as_view(), name='detail'),
    path('ajax/', include(ajax_urls)),
]
