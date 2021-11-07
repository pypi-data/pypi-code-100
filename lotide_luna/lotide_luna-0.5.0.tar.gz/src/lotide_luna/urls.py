from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timeline/<timeline_type>', views.timeline, name='timeline'),
    path('timeline/<timeline_type>/<page>',
         views.timeline, name='timeline_old'),
    path('communities', views.list_communities, name='communities'),
    path('communities/<int:community_id>',
         views.community, name='community'),
    path('communities/<int:community_id>/new',
         views.new_post, name='new_post'),
    path('communities/<int:community_id>/<page>',
         views.community, name='community_old'),
    path('users/<int:user_id>', views.user, name='user'),
    path('users/<int:user_id>/<page>', views.user, name='user_old'),
    path('posts/<int:post_id>', views.post, name='post'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
]
