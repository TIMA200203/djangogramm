from django.urls import path
from . import views
from users.views import follow_user

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/add_post/', views.add_post, name='add_post'),
    path('following/', views.posts_following_list, name='posts_following_list'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
]
