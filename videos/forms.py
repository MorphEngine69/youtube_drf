from django import forms

from .models import Video, Comment


class UploadVideoForm(forms.ModelForm):
    """Форма для загрузки/редактирования видео."""
    class Meta:
        model = Video
        fields = (
            'title',
            'description',
            'preview',
            'video',
        )


class CommentForm(forms.ModelForm):
    """Форма для создания комментария к видео."""
    class Meta:
        model = Comment
        fields = ('text',)
