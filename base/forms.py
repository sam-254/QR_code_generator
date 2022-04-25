from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class SignupForm(forms.ModelForm):
    """user signup form"""
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not confirm_password == password:
            self.add_error('confirm_password', 'Password does not match.')

        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("firstname", "lastname", "phone", "address")


class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


