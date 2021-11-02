from django.urls import path
from . import views

urlpatterns = [
    path('software-lifecycle-management/', views.SoftwareLifecycleManagementView.as_view(), name='index'),
]
