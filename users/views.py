from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.picture = form.cleaned_data.get('picture')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('videos:index')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})
