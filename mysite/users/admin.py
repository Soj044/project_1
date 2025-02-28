from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'is_staff', 'email', 'profile_photo', 'date_birth')
    list_filter = ("is_staff",)
    search_fields = ("username",)

    @admin.display(description='Фото профиля')
    def profile_photo(self, users: User):
        if users.photo:
            return mark_safe(f"<img src='{users.photo.url}'  width=50>")
        return "Без фото"





admin.site.register(User, CustomUserAdmin)
