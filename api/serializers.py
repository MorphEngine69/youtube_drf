from rest_framework import serializers

from videos.models import Video, Profile, Comment, Follow, LikeDislike


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализация модели для профиля пользователя."""
    picture = serializers.ImageField(
        required=False,
        default='default_avatar.png',
    )
    username = serializers.SerializerMethodField('get_profile_username', )

    @staticmethod
    def get_profile_username(model):
        return model.user.username

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'date_of_birth',
            'picture',
        ]
        read_only_fields = ['id', 'user', 'username', ]


class VideoSerializer(serializers.ModelSerializer):
    """Сериализация модели для видео."""
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'video',
            'pub_date',
            'author',
        ]
        read_only_fields = ['id', 'pub_date', 'author', ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация модели комментариев к видео."""
    author = ProfileSerializer(read_only=True)
    video_name = serializers.SerializerMethodField('get_video_name', )

    @staticmethod
    def get_video_name(model):
        return model.video.title

    class Meta:
        model = Comment
        fields = [
            'id',
            'video',
            'video_name',
            'text',
            'author',
            'pub_date',
        ]
        read_only_fields = ['id', 'video', 'pub_date', 'video_name', ]


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация модели подписки на пользователя."""
    username = serializers.SerializerMethodField('get_username')
    author_name = serializers.SerializerMethodField(
        'get_author_username')

    @staticmethod
    def get_username(model):
        return model.user.user.username

    @staticmethod
    def get_author_username(model):
        return model.author.user.username

    class Meta:
        model = Follow
        fields = [
            'id',
            'user',
            'username',
            'author',
            'author_name',
        ]
        read_only_fields = ['id', 'user', 'username', 'author_name', ]


class LikeDislikeSerializer(serializers.ModelSerializer):
    """Сериализация модели лайков/дизлайков к видео."""
    like = serializers.IntegerField(default=0, max_value=1, min_value=0)
    dislike = serializers.IntegerField(default=0, max_value=1, min_value=0)
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = LikeDislike
        fields = [
            'id',
            'like',
            'dislike',
            'author',
            'created',
        ]
        read_only_fields = ['id', 'created', 'video', 'author', ]

    def validate(self, data):
        if data['like'] == data['dislike']:
            raise serializers.ValidationError(
                'Оценки не могут быть одинаковыми!')
        return data
