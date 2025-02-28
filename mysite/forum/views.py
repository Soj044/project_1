from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
import uuid

from forum.forms import *
from forum.models import *
from django.template.loader import render_to_string

from forum.utils import DataMixin


class ForumHome(DataMixin, ListView):
    # model = Discussion
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Discussion.published.all().select_related('cat')


# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
# @login_required(login_url='users:login')
# def about(request):
#     if request.method == "POST":
#         form = UploadClassForm(request.POST, request.FILES)
#         if form.is_valid():
#             # handle_uploaded_file(form.cleaned_data['file'])
#             fp = UploadFiles(file=form.cleaned_data['file'])
#             fp.save()
#     else:
#         form = UploadClassForm()
#
#     return render(request, 'forum/about.html',
#                   {'title': "О форуме", 'form': form})

# def show_post(request, post_slug):
#     post = get_object_or_404(Discussion, slug=post_slug)
#     data = {'title': post.dis_title,
#             'menu': menu,
#             'post': post,
#             'cat_selected': 1}
#
#     return render(request, 'forum/post.html', data)

class ShowPost(DataMixin, DetailView):
    template_name = 'forum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, dis_title=context['post'].dis_title)

    def get_object(self, queryset=None):
        return get_object_or_404(Discussion.published, slug=self.kwargs[self.slug_url_kwarg])


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Discussion.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {'title': f"{category.name}",
#             'posts': posts,
#             'menu': menu,
#             'cat_selected': category.pk}
#
#     return render(request, 'forum/index.html', context=data)

class DiscusCategory(DataMixin, ListView):
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Discussion.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title="Category - " + cat.name, cat_selected=cat.pk)
        # context['title'] = "Category - " + cat.name
        # context['menu'] = menu
        # context['cat_selected'] = cat.pk
        # return context


class AddDiscuss(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'forum/addpost.html'
    # success_url = reverse_lazy('index')
    title_page = "Добавить обсуждение"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    # extra_context = {
    #     'title': "Добавить обсуждение",
    #     'menu': menu,
    #     'cat_selected': 0,
    #     'form': form_class
    # }


class UpdateDiscuss(DataMixin, UpdateView):
    model = Discussion
    fields = '__all__'
    template_name = 'forum/addpost.html'
    success_url = reverse_lazy('index')
    title_page = "Отредачить обсуждение"
    # extra_context = {
    #     'title': "Отредачить обсуждение",
    #     'menu': menu,
    # }


class DeleteDiscuss(DataMixin, DeleteView):
    model = Discussion
    context_object_name = 'post'  # ----------------ДОБАВИТЬ КНОПКУ ДЛЯ УДАЛЕНИЯ СТАТЬИ----------------
    success_url = reverse_lazy('index')
    template_name = 'forum/deletepage.html'
    title_page = "Удалить обсуждение"


def about(request):
    data = {
        'title': "О форуме",
        'text': f"this simple django beginner site, this is mt tg:"
    }
    return render(request, 'forum/about.html',
                  context=data)


def show_contact(request):
    return render(request, 'forum/socmedia.html', {'title': "Our social media"})
