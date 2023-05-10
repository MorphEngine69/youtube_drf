from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from embed_video.fields import EmbedVideoField

TODAY_DATE = date.today()

User = get_user_model()


def preview_to_user_path(instance, filename):
    """Загрузка превью по пути images/никнейм автора/превью/год/месяц."""

    return (
        'images/{username}/preview/{dt_year}/{dt_month}/{filename}'.format(
            username=instance.author,
            dt_year=TODAY_DATE.year,
            dt_month=TODAY_DATE.month,
            filename=filename,
        )
    )


def profile_picture_to_user_path(instance, filename):
    """Загрузка аватарок по пути images/никнейм автора/picture/год/месяц."""
    return (
        'images/{username}/profile_picture/{dt_year}/{dt_month}/{filename}'
        .format(
            username=instance.user,
            dt_year=TODAY_DATE.year,
            dt_month=TODAY_DATE.month,
            filename=filename,
        )
    )


class Profile(models.Model):
    """Модель для создания профиля."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Никнейм',
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения',
    )
    picture = models.ImageField(
        upload_to=profile_picture_to_user_path,
        verbose_name='Аватарка',
        blank=True,
        null=True,
        default='default_avatar.png',
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return '{username}'.format(
            username=self.user.username
        )


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Video(models.Model):
    """Модель для создания видео."""
    title = models.CharField(
        max_length=120,
        verbose_name='Название',
    )
    description = models.TextField(
        max_length=1024,
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    preview = models.ImageField(
        upload_to=preview_to_user_path,
        verbose_name='Превью',
    )
    video = EmbedVideoField(verbose_name='Ссылка на видео', )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Видеоролик'
        verbose_name_plural = 'Видеоролики'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для создания комментариев к видео."""
    video = models.ForeignKey(
        'Video',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Видео',
    )
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст комментария',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):
    """Модель для создания подписок на каналы."""
    user = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f'{self.user.user} -> {self.author.user}'
