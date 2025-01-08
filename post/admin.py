from django.contrib import admin
from .models import Content, Like


class ContentInline(admin.TabularInline):
    model = Content
    fk_name = 'parent'
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    fk_name = 'content'
    extra = 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_post", "created_at")
    list_filter = ("created_at",)
    inlines = [ContentInline, LikeInline]
    search_fields = ("content", "user__username")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    search_fields = ("user__username", "content__content")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content')
