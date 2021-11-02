try:
    from django.urls import include, path
    from rest_framework.routers import DefaultRouter

    from . import views

    router = DefaultRouter()
    router.register(r'faqs', views.FAQViewSet, 'faqs')
    router.register(r'front-data', views.FrontDataViewSet, 'front-data')
    router.register(r'front-data-std', views.StdFrontDataViewSet, 'front-data-std')
    router.register(r'front-data-full', views.FullFrontDataViewSet, 'front-data-full')

    urlpatterns = [
        path('', include(router.urls)),
    ]
except ModuleNotFoundError:
    urlpatterns = []
