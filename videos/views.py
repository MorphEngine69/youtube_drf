from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UploadVideoForm, CommentForm
from .models import Video, Profile, Comment, Follow, LikeDislike


def index(request):
    """Отвечает за отображение главной страницы."""
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'videos/index.html', context)


def profile(request, username):
    """Отвечает за отображение страницы с профилем."""
    get_profile = get_object_or_404(Profile, user__username=username)
    following = False
    if request.user.is_authenticated:
        request_profile = get_object_or_404(Profile, user=request.user)
        following = request_profile.follower.filter(author=get_profile)
    get_videos = Video.objects.filter(author=get_profile)
    follower_count = Follow.objects.filter(author=get_profile).count()
    context = {
        'profile': get_profile,
        'videos': get_videos,
        'following': following,
        'follower_count': follower_count,
    }
    return render(request, 'users/profile.html', context)


def video_detail(request, video_id):
    """Отвечает за отображение страницы с видео по его pk."""
    video = get_object_or_404(Video, pk=video_id)
    following = False
    if request.user.is_authenticated:
        request_profile = get_object_or_404(Profile, user=request.user)
        following = request_profile.follower.filter(author=video.author)
    likes = LikeDislike.objects.filter(video=video, like__gt=0)
    follower_count = Follow.objects.filter(author=video.author).count()
    comments = Comment.objects.filter(video=video)
    videos = Video.objects.all()
    user_avatar = video.author.picture

    context = {
        'video': video,
        'videos': videos,
        'likes': likes.count,
        'comments': comments,
        'picture': user_avatar,
        'following': following,
        'follower_count': follower_count,
    }
    return render(request, 'videos/video_detail.html', context)


@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.text = form.cleaned_data['text']
        comment.author = get_object_or_404(Profile, user=request.user)
        comment.video = video
        comment.save()
    return redirect('videos:video_detail', pk=video_id)


@login_required
def upload_video(request):
    """Отвечает за отображение страницы с формой загрузки видео."""
    form = UploadVideoForm(request.POST or None, files=request.FILES or None)
    if not request.method == 'POST':
        context = {
            'form': form,
            'is_edit': False,
        }
        return render(request, 'videos/upload_video.html', context)
    if not form.is_valid():
        return render(request, 'videos/upload_video.html', {
            'form': form, 'is_edit': False})
    video = form.save(commit=False)
    video.author = get_object_or_404(Profile, user=request.user)
    video.save()
    return redirect('videos:index')


@login_required
def edit_video(request, video_id):
    """Отвечает за отображение страницы с формой редактированием видео."""
    video = get_object_or_404(Video, pk=video_id)
    request_profile = get_object_or_404(Profile, user=request.user)
    form = UploadVideoForm(
        request.POST or None,
        files=request.FILES or None,
        instance=video,
    )
    context = {
        'form': form,
        'is_edit': True,
        'video': video,
    }
    if not video.author == request_profile and (
            request_profile.user.is_superuser is False
    ):
        return redirect(f'/watch/{video_id}/')
    if not request.method == 'POST':
        return render(request, 'videos/edit_video.html', context)
    if not form.is_valid:
        return render(request, 'videos/edit_video.html', context)
    video = form.save(commit=False)
    if request_profile.user.is_superuser is True:
        video.author = video.author
    else:
        video.author = request_profile

    video.save()
    return redirect(f'/watch/{video_id}/')


@login_required
def delete_video(request, video_id):
    """Отвечает за удаление видео из базы данных."""
    request_profile = get_object_or_404(Profile, user=request.user)
    video = get_object_or_404(Video, pk=video_id)
    if request_profile == video.author or request_profile.user.is_superuser:
        video.delete()
    return redirect('videos:index')


def follow_index(request):
    """Отвечает за отображение всех видео от авторов с подпиской от юзера."""
    request_profile = get_object_or_404(Profile, user=request.user)
    videos = Video.objects.filter(author__following__user=request_profile)
    context = {
        'videos': videos,
    }
    return render(request, 'videos/followed_videos.html', context)


@login_required
def profile_follow(request, username):
    """Отвечает за добавление подписки на автора."""
    request_profile = get_object_or_404(Profile, user=request.user)
    follow_author = get_object_or_404(Profile, user__username=username)
    if follow_author != request_profile and (
            not request_profile.follower.filter(author=follow_author)
    ):
        Follow.objects.create(
            user=request_profile,
            author=follow_author,
        )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_unfollow(request, username):
    """Отвечает за удаление подписки на автора."""
    request_profile = get_object_or_404(Profile, user=request.user)
    follow_author = get_object_or_404(Profile, user__username=username)
    data_follow = request_profile.follower.filter(author=follow_author)
    if data_follow.exists():
        data_follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def search_results(request):
    """Отвечает за отображение видео, где название == запросу."""
    search_text = request.GET.get('search')
    videos = Video.objects.filter(title__icontains=search_text)
    context = {
        'videos': videos,
    }
    return render(request, 'videos/search_results.html', context)


@login_required
def liked_index(request):
    request_profile = get_object_or_404(Profile, user=request.user)
    videos = Video.objects.filter(
        likedislike__author=request_profile, likedislike__like__gte=1)
    context = {
        'videos': videos,
    }
    return render(request, 'videos/liked_videos.html', context)


@login_required
def like_video(request, video_id):
    request_profile = get_object_or_404(Profile, user=request.user)
    video = get_object_or_404(Video, pk=video_id)
    ratings = LikeDislike.objects.filter(
        author=request_profile,
        video=video,
    )
    if not ratings.exists():
        ratings.create(
            like=1,
            video=video,
            author=request_profile,
        )
    else:
        for rating in ratings:
            if rating.dislike == 1:
                ratings.update(
                    like=1,
                    dislike=0,
                )
            else:
                ratings.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_video(request, video_id):
    request_profile = get_object_or_404(Profile, user=request.user)
    video = get_object_or_404(Video, pk=video_id)
    ratings = LikeDislike.objects.filter(
        author=request_profile,
        video=video,
    )
    if not ratings.exists():
        ratings.create(
            dislike=1,
            video=video,
            author=request_profile,
        )
    else:
        for rating in ratings:
            if rating.like == 1:
                ratings.update(
                    like=0,
                    dislike=1,
                )
            else:
                ratings.delete()

    return redirect(request.META.get('HTTP_REFERER'))
