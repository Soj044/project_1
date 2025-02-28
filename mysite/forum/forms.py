from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
import uuid
import os

from .models import Category, Discussion, Tracks




@deconstructible
class MyValidator:
    ALLOWED_CHARS = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁёйцукенгшщзхъфывапролджэячсмитьбю1234567890- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутсвовать1 только русские символы"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="не выбрана", label="Категория")
    tracks = forms.ModelChoiceField(queryset=Tracks.objects.all(), empty_label="не выбран", required=False,
                                    label="Трек(не обязательно)")

    class Meta:
        model = Discussion
        fields = ['dis_title', 'slug', 'dis_text', 'post_icon', 'is_published', 'cat', 'tracks']
        widgets = {
            'dis_title': forms.TextInput(attrs={'class': 'form-text'}),
        }
        labels = {'dis_title': 'Название', 'slug': 'URL', 'dis_text': 'Содержание', 'post_icon': 'Пикча'}


    def clean_dis_title(self):
        dis_title = self.cleaned_data['dis_title']
        if len(dis_title) > 50:
            raise ValidationError("Слишком длинное название")

        return dis_title

class UploadClassForm(forms.Form):
    file = forms.ImageField(label="File")
