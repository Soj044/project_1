from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from mysite import settings
from users.forms import LoginUsersForm, RegisterUsersForm, ProfielUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUsersForm
    template_name = 'users/login.html'
    extra_context = {'title': 'authorization'}

    """
        Редирект после авторизации юзера можно делать несколькими способами:
        1. С помощью переопределения функции get_success_url
        2. И в сеттингах с помощью LOGIN_REDIRECT_URL
        3. В шаблоне можно прописать <input type="hidden" name="next" value="{{next}}"/>
    """

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterUser(CreateView):
    form_class = RegisterUsersForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': "Registration"
    }


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfielUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile', 'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUsersForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # ПОПРОБОВАТЬ УБРАТЬ ЭТО(ЧТО БУДЕТ???)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUsersForm()
#     return render(request, 'users/register.html', {'form': form})


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUsersForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = LoginUsersForm()
#
#     return render(request, 'users/login.html', {'form': form})
