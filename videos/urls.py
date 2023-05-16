from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='index'),
    path('watch/<int:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('edit/<int:video_id>/', views.edit_video, name='edit_video'),
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('videos/<int:video_id>/comments/', views.add_comment,
         name='add_comment'),
    path('feed/subscriptions/', views.follow_index, name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    ),
    path('search/', views.search_results, name='search_results'),
    path('feed/liked/', views.liked_index, name='liked_videos'),
    path('watch/<int:video_id>/like/', views.like_video, name='like_video'),
    path(
        'watch/<int:video_id>/dislike/',
        views.dislike_video,
        name='dislike_video'),
]
