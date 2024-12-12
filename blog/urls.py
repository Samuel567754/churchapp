# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post listing and detail views
    path('blog/', views.blog, name='blog'),
    # path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_details, name='post_details'),
    # path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    
    # Category and Tag views
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
]
