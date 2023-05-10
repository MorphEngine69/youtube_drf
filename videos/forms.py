from django import forms

from .models import Video, Comment


class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = (
            'title',
            'description',
            'preview',
            'video',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
