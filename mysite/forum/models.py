import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

#   ----------------!!! ПЕРЕДЕЛАТЬ USER_ICON на POST_ICON !!!---------------------
#  Create your models here.

def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Discussion(models.Model):
    dis_title = models.CharField(max_length=200, default=None)
    dis_text = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    post_icon = models.ImageField(upload_to="icons/%Y/%m/%d", null=True,
                                  blank=True)
    vote = models.IntegerField(default=0, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, default=1)  # добавить related_name='posts'
    tracks = models.OneToOneField('Tracks', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='artist')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='dicuss', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.dis_title

    class Meta:
        verbose_name = "Обсуждения"
        verbose_name_plural = "Обсуждения"
        ordering = ['-pub_date']
        get_latest_by = "pub_date"
        indexes = [
            models.Index(fields=['-pub_date'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Это функция должна автоматом пишет слаг
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.dis_title)
    #     super().save(*args, **kwargs)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Tracks(models.Model):
    name = models.CharField(max_length=20, db_index=True)

    # slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self):
        return self.name

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')