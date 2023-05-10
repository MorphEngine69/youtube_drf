from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UploadVideoForm, CommentForm
from .models import Video, Profile, Comment, Follow


def index(request):
    """Отвечает за отображение главной страницы."""
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'videos/index.html', context)


def profile(request, username):
    """Отвечает за отображение страницы с профилем"""
    get_profile = get_object_or_404(Profile, user__username=username)
    request_profile = get_object_or_404(Profile, user=request.user)
    get_videos = Video.objects.filter(author=get_profile)
    following = False
    if request_profile.user.is_authenticated:
        following = request_profile.follower.filter(author=get_profile)
    follower_count = Follow.objects.filter(author=get_profile).count()
    context = {
        'profile': get_profile,
        'videos': get_videos,
        'following': following,
        'follower_count': follower_count,
    }
    return render(request, 'users/profile.html', context)


def video_detail(request, pk):
    """Отвечает за отображение страницы с видео по его pk."""
    video = get_object_or_404(Video, pk=pk)
    request_profile = get_object_or_404(Profile, user=request.user)
    following = False
    if request_profile.user.is_authenticated:
        following = request_profile.follower.filter(author=video.author)
    follower_count = Follow.objects.filter(author=video.author).count()
    comments = Comment.objects.filter(video=video)
    videos = Video.objects.all()
    user_avatar = video.author.picture

    context = {
        'video': video,
        'videos': videos,
        'comments': comments,
        'picture': user_avatar,
        'following': following,
        'follower_count': follower_count,
    }
    return render(request, 'videos/video_detail.html', context)


@login_required
def add_comment(request, pk):
    video = get_object_or_404(Video, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.text = form.cleaned_data['text']
        comment.author = get_object_or_404(Profile, user=request.user)
        comment.video = video
        comment.save()
    return redirect('videos:video_detail', pk=pk)


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
        return render(request, 'videos/upload_video,html', {
            'form': form, 'is_edit': False})
    video = form.save(commit=False)
    video.author = get_object_or_404(Profile, user=request.user)
    video.save()
    return redirect('videos:index')


@login_required
def edit_video(request, pk):
    """Отвечает за отображение страницы с формой редактированием видео."""
    video = get_object_or_404(Video, pk=pk)
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
        return redirect(f'/watch/{pk}/')
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
    return redirect(f'/watch/{pk}/')


@login_required
def delete_video(request, pk):
    """Отвечает за удаление видео из базы данных."""
    request_profile = get_object_or_404(Profile, user=request.user)
    video = get_object_or_404(Video, pk=pk)
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
