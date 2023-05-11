from django.contrib import admin
from .models import Video, Profile, Comment, Follow, LikeDislike


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Profile."""
    list_display = (
        'pk',
        'user',
        'date_of_birth',
        'picture',
    )
    list_editable = ('picture',)
    list_filter = ('date_of_birth',)
    search_fields = ('user',)
    empty_value_display = '-пусто-'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Video."""
    list_display = (
        'pk',
        'title',
        'pub_date',
        'description',
        'author',
        'preview',
        'video',

    )
    list_editable = ('title',)
    search_fields = (
        'title',
        'author',
        'pub_date',
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Comment."""
    list_display = (
        'pk',
        'video',
        'author',
        'text',
        'pub_date',
    )
    list_editable = ('text',)
    list_filter = ('pub_date',)
    search_fields = ('text', 'video',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели Follow."""
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    """Отвечает за отображение модели LikeDislike."""
    list_display = (
        'pk',
        'video',
        'like',
        'dislike',
        'created',
        'author',
    )
    list_editable = ('like', 'dislike',)
    list_filter = ('created',)
    search_fields = ('author', 'video',)
    empty_value_display = '-пусто-'
