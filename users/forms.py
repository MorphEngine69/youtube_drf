from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Дата рождения', required=False)
    picture = forms.ImageField(
        required=False,
        initial='default_avatar.png',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'picture',
            'date_of_birth',
            'password1',
            'password2',
        )
