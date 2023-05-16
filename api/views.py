from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from videos.models import Video, Profile, Follow, LikeDislike
from .permissions import IsAuthorOrReadOnly, IsProfileOrReadOnly
from .serializers import (VideoSerializer, ProfileSerializer,
                          CommentSerializer, FollowSerializer,
                          LikeDislikeSerializer)


class ProfileViewSet(ModelViewSet):
    """Вьюсет для обработки профиля пользователя."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['user__username', 'date_of_birth', ]

    def perform_create(self, serializer):
        serializer.save()


class VideoViewSet(ModelViewSet):
    """Вьюсет для обработки видео."""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    parser_classes = [MultiPartParser, JSONParser]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', 'author__user__username']

    def perform_create(self, serializer):
        request_profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(author=request_profile)


class CommentViewSet(ModelViewSet):
    """Вьюсет для обработки комментариев к видео."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['text', 'author__user__username', ]

    def get_queryset(self):
        video = get_object_or_404(Video, pk=self.kwargs.get('video_id'))
        return video.comments.all()

    def perform_create(self, serializer):
        request_profile = get_object_or_404(Profile, user=self.request.user)
        video = get_object_or_404(Video, pk=self.kwargs.get('video_id'))
        serializer.save(author=request_profile, video=video)


class FollowViewSet(ModelViewSet):
    """Вьюсет для обработки подписки на пользователя."""
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['author__user__username', ]

    def perform_create(self, serializer):
        request_profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(user=request_profile)


class LikeDislikeViewSet(ModelViewSet):
    """Вьюсет для обработки лайков/дизлайков на видео."""
    queryset = LikeDislike.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    serializer_class = LikeDislikeSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['author__user__username', ]

    def get_queryset(self):
        video = get_object_or_404(Video, pk=self.kwargs.get('video_id'))
        return video.likedislike.all()

    def perform_create(self, serializer):
        request_profile = get_object_or_404(Profile, user=self.request.user)
        video = get_object_or_404(Video, pk=self.kwargs.get('video_id'))
        if not video.likedislike.filter(author=request_profile):
            serializer.save(author=request_profile, video=video)
        else:
            raise ValidationError("Уже есть оценка у этого видео!")
