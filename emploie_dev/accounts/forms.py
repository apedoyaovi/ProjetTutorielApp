
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez le mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm_pwd = cleaned_data.get("confirm_password")
        if pwd != confirm_pwd:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
