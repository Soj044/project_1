from django import template
import forum.views as views
from forum.models import Category
from forum.utils import menu

register = template.Library()

@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag('forum/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}