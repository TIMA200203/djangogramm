from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('users/', views.users_list, name='users_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("following/<int:user_id>/", views.following_list, name="following_list"),
    path('register/', views.register, name='register'),
    path('profile/update/', views.profile_update, name='profile_update'),

    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]
