from django.contrib import admin
from django.core.checks import messages
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Discussion, Category, Tracks

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    fields = ['dis_title', 'slug', 'dis_text', 'is_published', 'cat', 'icon', 'tracks']
    # exclude = ['tracks']
    readonly_fields = ['icon']
    prepopulated_fields = {'slug': ('dis_title', )}
    list_display = ('dis_title', 'icon', 'pub_date', 'is_published', 'cat', 'tracks')
    list_display_links = ('dis_title',)
    list_editable = ('is_published', 'cat')
    ordering = ('pub_date',)
    actions = ['set_published', 'set_draft']
    search_fields = ['dis_title', 'cat__name']
    list_filter = ['cat__name', 'is_published']

    @admin.action(description="Опубликовать записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Изменено {count} записек")

    @admin.action(description="Убрать записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"Убрано {count} записек", messages.WARNING)

    @admin.display(description="Изображение")
    def icon(self, discus: Discussion):
        if discus.post_icon:
            return mark_safe(f"<img src='{discus.post_icon.url}'  width=50>")
        return "Без иконки"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Tracks)
class TracksAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ['name']

