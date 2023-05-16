from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (VideoViewSet, ProfileViewSet, CommentViewSet,
                    FollowViewSet, LikeDislikeViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'^video', VideoViewSet)
router.register(r'^profile', ProfileViewSet)
router.register(
    r'^video/(?P<video_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register(r'^follow', FollowViewSet, basename='follow')
router.register(
    r'^video/(?P<video_id>\d+)/likedislike',
    LikeDislikeViewSet,
    basename='likedislike',
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
