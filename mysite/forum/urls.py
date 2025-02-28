from django.urls import path
from . import views

urlpatterns = [path("", views.ForumHome.as_view(), name="index"),
               path("about/", views.about, name="about"),
               path("addpost/", views.AddDiscuss.as_view(), name="addpost"),
               path("socmedia/", views.show_contact, name="contact"),
               path("post/<slug:post_slug>", views.ShowPost.as_view(), name="post"),
               path("cat/<slug:cat_slug>", views.DiscusCategory.as_view(), name="category"),
               path("edit/<int:pk>", views.UpdateDiscuss.as_view(), name="editdiscuss"),
               path("delete/<int:pk>", views.DeleteDiscuss.as_view(), name="deletediscuss")]