import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUsersForm(AuthenticationForm):
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUsersForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'E-mail'}
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('this email already exists!')
        return email

class ProfielUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Name",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label="E-mail",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))
    photo = forms.ImageField(label='Avatar')

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth']
        labels = {
            'username': 'name',
            'email': 'e-mail',
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="old password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="new password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))