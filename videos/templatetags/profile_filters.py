from django import template
from django.shortcuts import get_object_or_404

from ..models import Profile

register = template.Library()


@register.filter
def get_profile(username):
    profile = get_object_or_404(Profile, user=username)
    if profile.picture == '':
        return 'none'
    else:
        return profile.picture.url
