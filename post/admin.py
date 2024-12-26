from django.contrib import admin
from .models import Post, AttachedImage, Comment, Like


class AttachedImageInline(admin.TabularInline):
    model = AttachedImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "content")
    inlines = [AttachedImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "content")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__content")


@admin.register(AttachedImage)
class AttachedImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image")
    list_filter = ("post__created_at",)
    search_fields = ("post__content",)
