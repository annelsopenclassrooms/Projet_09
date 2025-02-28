from django import forms

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):

        model = get_user_model()
        fields = ('username',)



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Masquer le help_text pour les champs de mot de passe
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None