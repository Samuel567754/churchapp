from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'featured', 'created_at', 'published_at', 'views_count')
    list_filter = ('is_published', 'featured', 'categories')
    search_fields = ('title', 'content', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'tags')
    actions = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        queryset.update(is_published=True, published_at=now())
        self.message_user(request, f"{queryset.count()} posts published successfully.")
    publish_posts.short_description = "Publish selected posts"

    def unpublish_posts(self, request, queryset):
        queryset.update(is_published=False, published_at=None)
        self.message_user(request, f"{queryset.count()} posts unpublished successfully.")
    unpublish_posts.short_description = "Unpublish selected posts"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('content', 'post__title', 'author__username')
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} comments approved successfully.")
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} comments disapproved successfully.")
    disapprove_comments.short_description = "Disapprove selected comments"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'liked_at')
    search_fields = ('post__title', 'user__username')
